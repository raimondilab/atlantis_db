import asyncio
import os
import aiomysql
import pandas as pd

# Database configuration
dsn = {
    'user': 'bionfolab',
    'password': 'Bioinfolab22#@!',
    'host': '127.0.0.1',
    'port': 3306,
    'db': 'integraR'
}

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


async def bulk_insert_contacts_async(table_name, columns, rows):
    if not rows:  # If there are no rows to insert, exit early
        return

    value_alias = "new_values"

    base_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES "
    values = []
    placeholders = []

    for row in rows:
        placeholders.append(f"({'%s, ' * (len(row) - 1) + '%s'})")
        values.extend(row)

    query = base_query + ", ".join(placeholders)
    update_assignments = "RESIDUE_ID = VALUES(RESIDUE_ID)"

    final_query = f"{query} AS {value_alias} ON DUPLICATE KEY UPDATE " + update_assignments

    await execute_query_with_retry_async(final_query, values)


async def get_record_id_async(pool, table, column, condition, values):
    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:
            query = f"SELECT {column} FROM {table} WHERE {condition}"
            await cursor.execute(query, values)
            result = await cursor.fetchone()
            return result[0] if result else None


async def process_file_and_insert(pool, files_folder, protein_an):

    file_path = os.path.join(files_folder, f"{protein_an}_pdb_contacts.txt")

    intra_rows = []
    inter_rows = []

    # Since the file exists, proceed with opening and processing it
    with open(file_path, 'r') as file:
        for line in file.readlines()[2:]:  # Skipping header lines
            parts = line.strip().split(" ")
            an_position = parts[0].strip()
            contacts = parts[1:]

            # Skip processing this line if there are no contacts
            if not contacts or contacts == ['']:
                continue

            # Fetch the residue_id for the given an_position
            residue_id = await get_record_id_async(pool, "RESIDUE", "RESIDUE_ID", "AN_POSITION = %s LIMIT 1", (an_position,))

            for contact in contacts:
                print(residue_id, protein_an)
                pdb_id, protein_of_contact, position = contact.split("_")
                if protein_of_contact == protein_an:
                    intra_rows.append((pdb_id, protein_of_contact, position, residue_id))
                else:
                    inter_rows.append((pdb_id, protein_of_contact, position, residue_id))

    # Perform bulk insertions for intra-molecular and inter-molecular contacts
    await bulk_insert_contacts_async("INTRA_MOLECULAR_CONTACT",
                                     ["PDB_ID", "PROTEIN_UID", "CONTACT_POSITION", "RESIDUE_ID"], intra_rows)
    await bulk_insert_contacts_async("INTER_MOLECULAR_CONTACT",
                                     ["PDB_ID", "PROTEIN_UID", "CONTACT_POSITION", "RESIDUE_ID"], inter_rows)


async def main():
    files_folder = "./PDB/"
    proteins = pd.read_csv("../data/proteins.csv")
    proteins_list = list(proteins['PROTEIN_AN'].unique())

    async with aiomysql.create_pool(**dsn) as pool:

        for protein_an in proteins_list:

            # Check if the file exists before processing
            if os.path.exists(os.path.join(files_folder, f"{protein_an}_pdb_contacts.txt")):
                await process_file_and_insert(pool, files_folder, protein_an)

    # Explicitly close the pool
    pool.close()
    await pool.wait_closed()

    # Ensure all changes are committed before exiting
    async with pool.acquire() as connection:
        await connection.commit()


if __name__ == "__main__":
    asyncio.run(main())
