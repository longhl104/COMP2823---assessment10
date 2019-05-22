import box
from union_interface import UnionInterface


class UnionBox(UnionInterface):
    """
    Union Box

    From a graph of boxes, get the union of boxes

    Example:
    4 |                   ______
    3 |     ____         |    __|_______________
    2 |   _|__  |    ____|   |  |               |
    1 |  | |  | |   |    |   |  |               |
    0 |__|_|__|_|___|____|___|__|_______________|________
         2 4  7 9   13   18  22 25              40

    union = [
        # Illustrates the first set of boxes:
        (2, 0), (2, 2), (4, 2), (4, 3), (9, 3), (9, 0),
        # Illustrates the second set of boxes:
        (13, 0), (13, 2), (18, 2), (18, 4), (25, 4), (25, 3), (40, 3), (40, 0)
    ]

    (Visual representation):

     4 |                    ______
     3 |      ____         |      |_______________
     2 |    _|    |    ____|                      |
     1 |   |      |   |                           |
     0 |___|______|___|___________________________|________
           2 4  7 9   13   18  22 25              40

    """
    @staticmethod
    def on_segment(p, q, r):
        if q[0] < max(p[0], r[0]) and q[0] > min(p[0], r[0]) and q[1] < max(p[1], r[1]) and q[1] > min(p[1], r[1]):
            return True
        return False

    @staticmethod
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1]);
        if val == 0:
            return 0
        if val > 0:
            return 1
        return 2

    @staticmethod
    def do_intersect(p1, q1, p2, q2):
        o1 = UnionBox.orientation(p1, q1, p2)
        o2 = UnionBox.orientation(p1, q1, q2)
        o3 = UnionBox.orientation(p2, q2, p1)
        o4 = UnionBox.orientation(p2, q2, q1)
        if o1 != o2 and o3 != o4:
            return True
        if o1 == 0 and UnionBox.on_segment(p1, p2, q1):
            return True
        if o2 == 0 and UnionBox.on_segment(p1, q2, q1):
            return True
        if o3 == 0 and UnionBox.on_segment(p2, p1, q2):
            return True
        if o4 == 0 and UnionBox.on_segment(p2, q1, q2):
            return True
        return False

    @staticmethod
    def is_inside(polygon, n, p):
        extreme = (1e9, p[1])
        count = 0
        i = 0
        while True:
            next = (i+1)%n
            if UnionBox.do_intersect(polygon[i], polygon[next], p, extreme):
                if UnionBox.orientation(polygon[i], p, polygon[next]) == 0:
                    return UnionBox.on_segment(polygon[i], p, polygon[next])
                count += 1
            i = next
            if i == 0:
                break
        return count&1

    @staticmethod
    def separate(polygon):
        res = []
        tmp = []
        for i in range(len(polygon)-1):
            if polygon[i][1] == polygon[i+1][1] == 0:
                tmp += [polygon[i]]
                res += [tmp]
                tmp = []
            else:
                tmp += [polygon[i]]
        tmp += [polygon[-1]]
        res += [tmp]
        return res

    @staticmethod
    def take_first(elem):
        return elem[0]

    @staticmethod
    def expand(l):
        i = 0
        while i < len(l) - 1:
            ext = []
            if l[i][0] == l[i+1][0]:
                if l[i][1] < l[i+1][1]:
                    for j in range(l[i][1]+1, l[i+1][1]):
                        ext += [(l[i][0], j)]
                else:
                    for j in range(l[i][1]-1, l[i+1][1], -1):
                        ext += [(l[i][0], j)]
            else:
                if l[i][0] < l[i+1][0]:
                    for j in range(l[i][0]+1, l[i+1][0]):
                        ext += [(j, l[i][1])]
                else:
                    for j in range(l[i][0]-1, l[i+1][0], -1):
                        ext += [(j, l[i][1])]
            l = l[:i+1]+ext+l[i+1:]
            i += len(ext) + 1
        return l

    def merge(self, l, r):
        """
        Merge the two "boxes" together.
           ____           ____
         _|__  |              |
        | |  | |  ==>  |      |
        |_|__|_|       |      |

        Example:
        input:
            l: [ (2,0), (2,2), (7,2), (7,0) ]
            r: [ (4,0), (4,3), (9,3), (9,0) ]
        return:
            [ (2,0), (2,2), (4,2), (4,3), (9,3), (9,0) ]

        :param l: Array of coordinates representing one box.
        :param r: Array of coordinates representing another box.
        :return: The merged coordinates to present.
        """
        # TODO implement me.
        if l[0][0] > r[0][0]:
            tmp = l
            l = r
            r = tmp
        if l[-1][0] < r[0][0]:
            return l+r
        oldl = l
        oldr = r
        l = UnionBox.expand(l)
        r = UnionBox.expand(r)
        res = []
        for i in range(len(l)):
            polygons = UnionBox.separate(oldr)
            add = 1
            for j in range(len(polygons)):
                if UnionBox.is_inside(polygons[j], len(polygons[j]), l[i]) != 0:
                    add = 0
            if add == 1:
                res += [l[i]]
        for i in range(len(r)):
            polygons = UnionBox.separate(oldl)
            add = 1
            for j in range(len(polygons)):
                if UnionBox.is_inside(polygons[j], len(polygons[j]), r[i]) != 0:
                    add = 0
            if add == 1 and (r[i] in res) == 0:
                res += [r[i]]
        res.sort(key=UnionBox.take_first)
        i = 0
        while i < len(res) - 1:
            if i>0 and res[i-1][1] == res[i][1] == res[i+1][1]:
                res = res[:i] + res[i+1:]
                continue
            if i>0 and res[i-1][0] == res[i][0] == res[i+1][0]:
                res = res[:i] + res[i+1:]
                continue
            if i>0 and res[i-1][1] > res[i][1] and res[i+1][1] > res[i][1]:
                res = res[:i] + res[i+1:]
                continue
            i+=1
        i = 0
        while i < len(res) - 1:
            if res[i][0] != res[i+1][0] and res[i][1] != res[i+1][1]:
                if res[i][1] < res[i+1][1]:
                    res = res[:i+1] + [(res[i+1][0], res[i][1])] + res[i+1:]
                    i += 1
                else:
                    res = res[:i+1] + [(res[i][0], res[i+1][1])] + res[i+1:]
                    i += 1
            i += 1
        i = 0
        while i < len(res) - 1:
            if i>0 and res[i-1][1] == res[i][1] == res[i+1][1]:
                res = res[:i] + res[i+1:]
                continue
            if i>0 and res[i-1][0] == res[i][0] == res[i+1][0]:
                res = res[:i] + res[i+1:]
                continue
            if i>0 and res[i-1][1] > res[i][1] and res[i+1][1] > res[i][1]:
                res = res[:i] + res[i+1:]
                continue
            i+=1
        return res

    def union(self, box_list):
        """
        Performs the union of a list of boxes (in the form of x, y coordinate tuples)

        e.g. box_list = [ [(2,2), (2, 2), (7, 2), (7, 0)], [(4,0), (4,3), (9,3), (9,0)] ]
        :param box_list: List of boxes represented as coordinates.
        :return: The union of all the boxes.  (As presented in the example above)
        """
        if not box_list:
            return []

        if len(box_list) == 1:
            return box_list[0]

        if len(box_list) == 2:
            left_box = box_list[0]
            right_box = box_list[1]
            merged = self.merge(left_box, right_box)
            return merged

        # Else, time to do me a recursion
        left_list = self.union(box_list[:int(len(box_list) / 2)])
        right_list = self.union(box_list[int(len(box_list) / 2):])
        merged = self.merge(left_list, right_list)
        return merged

if __name__ == '__main__':
    box_list = [ [(2,0), (2, 2), (7, 2), (7, 0)], [(4,0), (4,3), (9,3), (9,0)] ]
    box_list2 = [
        [(0,0), (0,2), (2,2), (2,1), (4,1), (4,0)],
        [(1,0), (1,3), (3,3), (3,0)]
    ]
    box_list3 = [
        [(1,0), (1,1), (30,1), (30,0)],
        [(5,0), (5,2), (9,2), (9,0)],
        [(16,0), (16,3), (27,3), (27, 0)]
    ]
    a = UnionBox()
    print(a.union(box_list))
