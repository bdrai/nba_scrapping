class Stats:
    min: int
    fgm: int
    fga: int
    three_pts_m: int
    three_pts_a: int
    ftm: int
    fta: int
    oreb: int
    dreb: int
    reb: int
    ast: int
    stl: int
    blk: int
    to: int
    pf: int
    plus_minus: int
    pts: int

    def __init__(self, stats):
        stats_list = self.process_stats(stats)
        self.min = stats_list[0]
        self.fgm = stats_list[1]
        self.fga = stats_list[2]
        self.three_pts_m = stats_list[3]
        self.three_pts_a = stats_list[4]
        self.ftm = stats_list[5]
        self.fta = stats_list[6]
        self.oreb = stats_list[7]
        self.dreb = stats_list[8]
        self.reb = stats_list[9]
        self.ast = stats_list[10]
        self.stl = stats_list[11]
        self.blk = stats_list[12]
        self.to = stats_list[13]
        self.pf = stats_list[14]
        self.plus_minus = stats_list[15]
        self.pts = stats_list[16]

    @staticmethod
    def process_stats(stats_list):
        """Manages the proportion stats, for example FGM/FGA to split it"""
        output = []
        for elt in stats_list:
            try:
                value = int(elt)
                output.append(value)
            except ValueError:
                if elt == '--':
                    output.append(0)
                elif elt == '-----':
                    output.append(0)
                    output.append(0)
                elif '-' in elt:
                    value = elt.split('-')
                    output += [*value]
        return output

    def export_stats_in_list(self):
        """Return the statistics onto a list"""
        return [
            self.min, self.fgm, self.fga, self.three_pts_m, self.three_pts_a,
            self.ftm, self.fta, self.oreb, self.dreb, self.reb, self.ast,
            self.stl, self.blk, self.to, self.pf, self.plus_minus, self.pts
        ]
