import utils.normalization.normalization_ch as normalizer_ch


def normalize_address(address, structure_sign="", lang="ch"):
    if lang == "ch":
        normalized_address = normalizer_ch.normalize_address(address,
                                                     structure_sign=structure_sign)
    return normalized_address


