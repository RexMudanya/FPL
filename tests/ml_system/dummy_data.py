from pandas import DataFrame

good_df = DataFrame(
    [
        ["DEF", "50", "True", "100", "1", "0", "3", "1", "xyz abc"],
        ["MID", "40", "False", "10", "1", "1", "5", "0", "xy2z a4bc"],
        ["MID", "90", "True", "70", "1" "0", "3", "1", "gdf gsbc"],
        ["DEF", "60", "False", "80", "1", "1", "3", "1", "eyz abb"],
        ["MID", "50", "False", "10", "1", "10", "8", "1", "12s3 f456"],
        ["FWD", "100", "True", "400", "1", "10", "0", "0", "hbvfh duhfid"],
        ["GKP", "100", "False", "10", "1", "0", "0", "6", "jnfijf ijf"],
        ["FWD", "100", "True", "300", "1", "2", "2", "1", "jhid kosd"],
        ["FWD", "100", "False", "50", "1", "9", "4", "1", "hg abhgf"],
        ["GKP", "30", "False", "20", "1", "0", "0", "6", "45fd af5bc"],
    ],
    columns=[
        "position",
        "value",
        "was_home",
        "total_points",
        "GW",
        "goals_scored",
        "assists",
        "clean_sheets",
        "name",
    ],
)
