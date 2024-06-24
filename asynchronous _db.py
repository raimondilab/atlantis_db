import asyncio
import aiomysql
import pandas as pd
import os

dsn = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'db': os.getenv('DB_NAME')
}


async def get_record_id_async(pool, table, column, condition, values):
    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:
            query = f"SELECT {column} FROM {table} WHERE {condition}"
            await cursor.execute(query, values)
            result = await cursor.fetchone()
            return result[0] if result else None


# Read residue's information
def read_file_residue_rows(path):
    columns = [
        "AN_POSITION", "UN_REF_PROT_RE", "AF_RES", "UN_ANN_NAT_VARIANTS",
        "UN_MOLECULE_PROCESSING", "UN_LOCATION", "UN_MOTIVES", "UN_DOMAINS",
        "PFAM_DOMAIN_POS_HMM", "UN_LIGANDS_BINDING_SITE", "UN_ANN_PROP_ACTIVE_SITE",
        "PHOS_PTMS", "UN_GLYCOSYLATIONS", "UN_LIPIDATIONS", "UN_MODIFIED_RES",
        "UN_DISULFIDE_BONG_BRIDGES", "UN_SECONDARY_STRUCTURE",
        "AF_PREDICTED_SECONDARY_STRUCTURE", "AF_CONFIDENCE_VALUE",
        "AF_MAX_PREDICTED_NUM_INTERACTION_RESIDUE", "AF_RESIDUE_PREDICTED_INTERACTION", "UN_CROSS_LINKS", "PROTEIN_ID"
    ]

    try:
        # Read the data into a pandas DataFrame
        df = pd.read_csv(path, delimiter='|', skiprows=31, names=columns)

        # Define a regular expression pattern to extract strings
        pattern = r":\s*\[?\s*([^|\]]+)?\s*\]?"

        # Apply the pattern to each column of the DataFrame
        for col in df.columns[1:]:
            df[col] = df[col].astype(str).str.extract(pattern, expand=False)

    except FileNotFoundError:
        print(f"The file '{path}' does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    return df


MAX_RETRIES = 20


async def execute_query_with_retry_async(query, data=None, retry_count=0):
    try:
        async with aiomysql.create_pool(**dsn) as pool:
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    if data is not None:
                        await cursor.execute(query, data)
                    else:
                        await cursor.execute(query)
                    await connection.commit()
    except aiomysql.Error as err:
        if "Deadlock" in str(err) and retry_count < MAX_RETRIES:
            print(f"Deadlock detected. Retrying... (Retry count: {retry_count + 1})")
            await asyncio.sleep(1)
            await execute_query_with_retry_async(query, data, retry_count + 1)
        else:
            print(f"Aiomysql error: {err}")


async def insert_residues_async(table_name, columns, rows):
    value_alias = "new_values"

    base_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES "
    values = []
    placeholders = []

    for row in rows:
        placeholders.append(f"({'%s, ' * (len(row) - 1) + '%s'})")
        values.extend(row)

    query = base_query + ", ".join(placeholders)
    update_assignments = [f"{col}={value_alias}.{col}" for col in columns]

    final_query = f"{query} AS {value_alias} ON DUPLICATE KEY UPDATE " + ", ".join(update_assignments)

    await execute_query_with_retry_async(final_query, values)


async def process_file_async(files_folder, file_path, protein_id):
    df = read_file_residue_rows(files_folder + file_path)

    columns = [
        "AN_POSITION", "UN_REF_PROT_RE", "AF_RES", "UN_ANN_NAT_VARIANTS",
        "UN_MOLECULE_PROCESSING", "UN_LOCATION", "UN_MOTIVES", "UN_DOMAINS",
        "PFAM_DOMAIN_POS_HMM", "UN_LIGANDS_BINDING_SITE", "UN_ANN_PROP_ACTIVE_SITE",
        "PHOS_PTMS", "UN_GLYCOSYLATIONS", "UN_LIPIDATIONS", "UN_MODIFIED_RES",
        "UN_DISULFIDE_BONG_BRIDGES", "UN_SECONDARY_STRUCTURE",
        "AF_PREDICTED_SECONDARY_STRUCTURE", "AF_CONFIDENCE_VALUE",
        "AF_MAX_PREDICTED_NUM_INTERACTION_RESIDUE", "AF_RESIDUE_PREDICTED_INTERACTION", "UN_CROSS_LINKS", "PROTEIN_ID"
    ]

    batch_size = 1000
    batch = []

    for index, row in df.iterrows():

        data = (
            row['AN_POSITION'].strip(), row['UN_REF_PROT_RE'].strip(), row['AF_RES'].strip(), row['UN_ANN_NAT_VARIANTS'].strip(),
            row['UN_MOLECULE_PROCESSING'].strip(), row['UN_LOCATION'].strip(), row['UN_MOTIVES'].replace('"', "").strip(),
            row['UN_DOMAINS'].replace('"', "").strip(), row['PFAM_DOMAIN_POS_HMM'].strip(),
            row['UN_LIGANDS_BINDING_SITE'].replace('"', "").strip() if row['UN_LIGANDS_BINDING_SITE'] else row[
                'UN_LIGANDS_BINDING_SITE'].strip(),
            row['UN_ANN_PROP_ACTIVE_SITE'].replace('"', "").strip() if row['UN_ANN_PROP_ACTIVE_SITE'] else row[
                'UN_ANN_PROP_ACTIVE_SITE'].strip(),
            row['PHOS_PTMS'].replace('"', "").strip() if row['PHOS_PTMS'] else "no_ptms",
            row['UN_GLYCOSYLATIONS'].replace('"', "").strip() if row['UN_GLYCOSYLATIONS'] else row['UN_GLYCOSYLATIONS'].strip(),
            row['UN_LIPIDATIONS'].replace('"', "").strip() if row['UN_LIPIDATIONS'] else row['UN_LIPIDATIONS'].strip(),
            row['UN_MODIFIED_RES'].replace('"', "").strip() if row['UN_MODIFIED_RES'] else row['UN_MODIFIED_RES'].strip(),
            row['UN_DISULFIDE_BONG_BRIDGES'].strip(), row['UN_SECONDARY_STRUCTURE'].strip(),
            row['AF_PREDICTED_SECONDARY_STRUCTURE'].strip(),
            float(row['AF_CONFIDENCE_VALUE']) if type(row['AF_CONFIDENCE_VALUE']) != str else 0,
            int(row['AF_MAX_PREDICTED_NUM_INTERACTION_RESIDUE']) if type(
                row['AF_MAX_PREDICTED_NUM_INTERACTION_RESIDUE']) != str else 0,
            row["AF_RESIDUE_PREDICTED_INTERACTION"].strip() if row["AF_RESIDUE_PREDICTED_INTERACTION"] else "no_af_residues",
            row['UN_CROSS_LINKS'], int(protein_id)
        )

        batch.append(data)

        if len(batch) >= batch_size:
            await insert_residues_async("RESIDUE", columns, batch)
            batch = []  # Resetando o lote após a inserção

    if batch:
        await insert_residues_async("RESIDUE", columns, batch)


async def main():
    files_folder = "./database/"
    files = os.listdir(files_folder)

    async with aiomysql.create_pool(**dsn) as pool:
        for file_path in files:
            protein = str(file_path.split("_")[0])
            protein_id = await get_record_id_async(pool, "PROTEIN", "PROTEIN_ID", "PROTEIN_AN= %s", (protein,))
            print(protein, protein_id)

            # Insert all rows of a file at a time
            if protein_id:
                await process_file_async(files_folder, file_path, protein_id)

        # Explicitly close the pool
        pool.close()
        await pool.wait_closed()

        # Ensure all changes are committed before exiting
        async with pool.acquire() as connection:
            await connection.commit()


if __name__ == "__main__":
    asyncio.run(main())
