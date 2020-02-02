def build_lookup_from_csv(
        table_path, key_field, to_lower=True, warn_if_missing=True):
    """Read a CSV table into a dictionary indexed by `key_field`.

    Creates a dictionary from a CSV whose keys are unique entries in the CSV
    table under the column named by `key_field` and values are dictionaries
    indexed by the other columns in `table_path` including `key_field` whose
    values are the values on that row of the CSV table.

    Parameters:
        table_path (string): path to a CSV file containing at
            least the header key_field
        key_field: (string): a column in the CSV file at `table_path` that
            can uniquely identify each row in the table.
        to_lower (bool): if True, converts all unicode in the CSV,
            including headers and values to lowercase, otherwise uses raw
            string values.
        warn_if_missing (bool): If True, warnings are logged if there are
            empty headers or value rows.

    Returns:
        lookup_dict (dict): a dictionary of the form {
                key_field_0: {csv_header_0: value0, csv_header_1: value1...},
                key_field_1: {csv_header_0: valuea, csv_header_1: valueb...}
            }

        if `to_lower` all strings including key_fields and values are
        converted to lowercase unicode.

    """
    table = pandas.read_csv(table_path, sep=None, engine='python')
    header_row = list(table)
    if to_lower:
        key_field = key_field.lower()
        header_row = [
            x if not isinstance(x, str) else x.lower()
            for x in header_row]

    if key_field not in header_row:
        raise ValueError(
            '%s expected in %s for the CSV file at %s' % (
                key_field, header_row, table_path))
    if warn_if_missing and '' in header_row:
        LOGGER.warn(
            "There are empty strings in the header row at %s", table_path)

    key_index = header_row.index(key_field)
    lookup_dict = {}
    for index, row in table.iterrows():
        if to_lower:
            row = pandas.Series([
                x if not isinstance(x, str) else x.lower()
                for x in row])
        # check if every single element in the row is null
        if row.isnull().values.all():
            LOGGER.warn(
                "Encountered an entirely blank row on line %d", index+2)
            continue
        if row.isnull().values.any():
            row = row.fillna('')
        lookup_dict[row[key_index]] = dict(zip(header_row, row))
    return lookup_dict
