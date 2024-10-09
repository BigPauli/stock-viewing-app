from sqlalchemy import create_engine, text

path = "../data/info.db"

def get_column_from_company(col_name="*", *, flatten=False):
    conn = create_engine(f"sqlite:///{path}").connect()

    query = text(f"SELECT {col_name} FROM companies")
    data = conn.execute(query)
    conn.close()
    if flatten:
        # https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
        return [value for tup in list(data) for value in tup]
    return data


if __name__ == "__main__":
    print(list(get_column_from_company()))
    print(list(get_column_from_company("name")))
    print(list(get_column_from_company("symbol")))
    print(get_column_from_company("name", flatten=True))