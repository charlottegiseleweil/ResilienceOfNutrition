import np as np

def convert_production_tons_to_caloric(crop_prod_array, calories_per_ton, nodata):
    """Calorie (i) production = Crop (i) production x KJ content of crop (i).

    Parameters:
        crop_prod_array (array): production in tons.
        calories_per_ton (float): calories/ton accounting for % refuse
            of the crop.
        nodata (float): nodata value for `crop_prod_array` and result.

    Returns:
        calorie production production * calories / ton

    """
    result = np.array(crop_prod_array)
    result[~np.isclose(crop_prod_array, nodata)] *= calories_per_ton
    return result

def div_arrays_op(numerator_array, denominator_array, nodata):
    """Calculate calorie yield.

    Parameters:
        numerator
        e.g total_calorie_array (np.ndarray): total calories per element
        denominator
        e.g harvested_area_ha_array (np.ndarray): amount of total harvested
            area in hectares per eleent.
        nodata (float): the nodata value for all inputs and result.

    Returns:
        divided
        e.g calorie yield = total calorie production / sum(harvested area)

    """
    result = np.empty_like(numerator_array)
    result[:] = nodata
    zero_mask = (denominator_array == 0.0)
    valid_mask = (
        ~np.isclose(numerator_array, nodata) &
        ~np.isclose(denominator_array, nodata)) & ~zero_mask
    result[valid_mask] = (
        numerator_array[valid_mask] / (
            denominator_array[valid_mask]))
    result[zero_mask] = 0.0
    return result




def crop_production_op(
        yield_array, prop_harvest_area, cell_area_ha,
        prop_harvest_area_nodata, target_nodata):
    """Calculate crop production

    Parameters:
        yield_array (np.ndarray): yield of crop in Tons/Ha
        prop_harevest_area (np.ndarray): proportional harvested area of
            the crop per cell.
        cell_harea_ha (np.ndarray): area of the cell in Ha.
        prop_harvest_area_nodata (float): nodata value for prop_harevest_area
        target_nodata (float): nodata value for result

    Returns:
        Crop production =
            Yield(i) x harvested area (proportion) (i) * area of cell.

    """
    crop_production = np.empty_like(yield_array, dtype=np.float32)
    crop_production[:] = target_nodata
    valid_mask = ~np.isclose(prop_harvest_area, prop_harvest_area_nodata)
    crop_production[valid_mask] = (
        yield_array[valid_mask] * prop_harvest_area[valid_mask] *
        cell_area_ha[valid_mask])
    return crop_production

def mult_arrays_op(nodata, *array_list):
    """Multiply array stack and ignore nodata."""
    result = np.ones(array_list[0].shape, dtype=np.float32)
    valid_mask = np.empty(result.shape, dtype=np.bool)
    valid_mask[:] = False
    for array in array_list:
        local_valid_mask = ~np.isclose(array, nodata)
        valid_mask |= local_valid_mask
    for array in array_list:
        result[valid_mask] *= array[valid_mask]
    result[~valid_mask] = nodata
    return result


def sum_arrays_op(nodata, *array_list):
    """Sum all rasters assuming they all have the same nodata value."""
    result = np.zeros(array_list[0].shape, dtype=np.float32)
    valid_mask = np.empty(result.shape, dtype=np.bool)
    valid_mask[:] = False
    for array in array_list:
        local_valid_mask = ~np.isclose(array, nodata)
        valid_mask |= local_valid_mask
        result[local_valid_mask] += array[local_valid_mask]
    result[~valid_mask] = nodata
    return result

def calories_yield_op(total_calorie_array, harvested_area_ha_array, nodata):
    """Calculate calorie yield.

    Parameters:
        total_calorie_array (np.ndarray): total calories per element
        harvested_area_ha_array (np.ndarray): amount of total harvested
            area in hectares per eleent.
        nodata (float): the nodata value for all inputs and result.

    Returns:
        calorie yield = total calorie production / sum(harvested area)

    """
    result = np.empty_like(total_calorie_array)
    result[:] = nodata
    zero_mask = (harvested_area_ha_array == 0.0)
    valid_mask = (
        ~np.isclose(total_calorie_array, nodata) &
        ~np.isclose(harvested_area_ha_array, nodata)) & ~zero_mask
    result[valid_mask] = (
        total_calorie_array[valid_mask] / (
            harvested_area_ha_array[valid_mask]))
    result[zero_mask] = 0.0
    return result