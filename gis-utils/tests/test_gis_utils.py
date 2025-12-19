import pytest

import gis_utils


class TestPolylineStrToCoords:
    def setup_method(self):
        # Strava segment Re Stelvio Mapei, segment-id 15104529341.
        self.polyline = r"abszGqhh~@s@nD{F~I{HbE_@AQeAzBqIYk@qGpEiEn@sPmBlG{EeGeAmBiCqIdF{IAgCdBwAdDeEdC}A~CiEi@cC_BwKpHqPlC}CvDuAdDgC`@gB~CBlC]bA{DbCuDbEcBXmA~AoBEkNxAqClCiCt@}GQqDpAuAc@uEoNoGiLVSfEtEwDeIaE}OeGcMNQ|D`FyDsJAwE}@kED}AcC}EmAc@}BsD_@yIeC_IUqDfBvEk@eF^lB`AhBZAqAoEQoEHeBvAqAPkSdAgH[_Lf@cDmBoQ@uDf@uBuAgCGyEoB_Ja@mJsCwD}AuEoCcEeDyLwEaH?e@l@BlD`DXOoBmCcA}CkByAxBj@nAvBR[yGiMgDCzByByEp@zFmFyFt@aCjB~AmD`EmCG[gGlAyCxFpBeJbFqCf@eAkInCoAbCsF|DSg@bA}F`EsCcL|B}LwB{BoA}D|CiCs@sLlBuAOiFwD{CMqElAqKw@aKuEkDeG{FOyCmDwE}@cKeQsA_EgDex@f@oJx@_GtBoGhIsI}GhAdJeKgE`@kCrAtAaEfHeEjByFdGmFs@{BjNyAdHiDgFaMC{AbBgDtEyB`AiDu@y@kGv@Wa@LkAdDcIb@iGzE\jC~CZcAsAyEpGeAy@gLuA[tGeJ~EE@cC}@}BtAwKFjA{ApIv@~APxBu@rAmDs@kHzIzAt@`AnKuGhAjAtEWbAcCwCaFg@c@pGgDjIIfAZj@dGw@r@h@aAhD_FjCuAxCNpBtElLmGzC{N|Al@fCcGbFcBzFcHbE}BlETd@hCqBjEi@iJzJTd@lGeBsIvIwAzDmAzGi@`MpCvt@x@dEdLpSjFhA`DvDvFJdDtFtKjF~Jj@`FoAtCPvGjEhMyBhCx@`E_D|AlAlMtBbLiCuDzAuAzHVn@rFoDvBmDnGcBaG|DqBxI`@TpCsFzFwAoE~CyAfCDl@dKcDcGnFbFi@}BrB~DXpGpLyAiBmCc@hBhB|@rCvBtCqDuCw@IKj@`FhH~DnNjBpBhBnF`ChCTfJdAjC~DfT_ArAApB`AtM?hLx@vEa@hEy@zAc@hMcBhNNdDxAdFaCaFr@dFkBwETxE|BlGb@bJdCfE`GrBaAfB?bBdAxEAfEzD|JsDeFYVpG`NdDxMlEjJkEyEU^lElHpFzMp@zC|Ad@hDwA~GL`Cu@dCoCrNwAlBNrD{B|JyIJsDpB_EzBSlFwIhPiC|K{HxCfBzDf@dBmDfEcChAmCtBeBjJIfH}ElAJjAdB~FlAyBxBiC`APz@pSpAdCs@lF_EJx@yBfIN|@n@@hGsCjGiJbAwBl@sIxBsDbD]fIfFk@qCv@_FtHeB"

    def test_happy_flow(self):
        coords = gis_utils.polyline_str_to_coords(self.polyline)
        assert len(coords) == 349
        assert coords[0] == (46.46961, 10.36953)
        assert coords[348] == (46.46477, 10.37296)

    # Update: I removed the `precision` arg because confusing.
    # def test_precision_6(self):
    #     coords = gis_utils.polyline_str_to_coords(
    #         self.polyline,
    #         precision=6,
    #     )
    #     assert len(coords) == 349
    #     assert coords[0] == (4.646961, 1.036953)
    #     assert coords[348] == (4.646477, 1.037296)
    #
    # Update: I removed the `precision` arg because confusing.
    # def test_precision_7(self):
    #     coords = gis_utils.polyline_str_to_coords(
    #         self.polyline,
    #         precision=7,
    #     )
    #     assert len(coords) == 349
    #     assert coords[0] == (0.4646961, 0.1036953)
    #     assert coords[348] == (0.4646477, 0.1037296)

    def test_not_a_str(self):
        with pytest.raises(TypeError):
            gis_utils.polyline_str_to_coords(123)


class TestComputeGreatCircleDistance:
    def setup_method(self):
        self.a = (46.46961, 10.36953)  # Bormio.

    def test_example_from_wikipedia(self):
        # Src: https://en.wikipedia.org/wiki/Haversine_formula#Example
        white_house = (38.898, -77.037)
        eiffel_tower = (48.858, 2.294)

        dist1 = gis_utils.compute_great_circle_distance(
            white_house[0], white_house[1], eiffel_tower[0], eiffel_tower[1]
        )
        dist2 = gis_utils.compute_great_circle_distance(
            eiffel_tower[0], eiffel_tower[1], white_house[0], white_house[1]
        )
        assert dist1 == dist2
        assert round(dist1, 2) == round(6161.438034825137, 2)

    def test_example_from_scikit(self):
        # Src: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.haversine_distances.html
        bsas = (-34.83333, -58.5166646)  # Ezeiza Airport (Buenos Aires, Argentina).
        paris = (49.0083899664, 2.53844117956)  # C. de Gaulle Airport (Paris, France).

        dist1 = gis_utils.compute_great_circle_distance(
            bsas[0], bsas[1], paris[0], paris[1]
        )
        dist2 = gis_utils.compute_great_circle_distance(
            paris[0], paris[1], bsas[0], bsas[1]
        )
        assert dist1 == dist2
        assert round(dist1, 2) == round(11099.54035581966, 2)

    def test_example_from_geopy(self):
        # Src: https://github.com/geopy/geopy?tab=readme-ov-file#measuring-distance
        newport_ri = (41.49008, -71.312796)
        cleveland_oh = (41.499498, -81.695391)

        dist1 = gis_utils.compute_great_circle_distance(
            newport_ri[0], newport_ri[1], cleveland_oh[0], cleveland_oh[1]
        )
        dist2 = gis_utils.compute_great_circle_distance(
            cleveland_oh[0], cleveland_oh[1], newport_ri[0], newport_ri[1]
        )
        assert dist1 == dist2
        assert round(dist1, 2) == round(864.2144943386634, 2)

    def test_north(self):
        dist = gis_utils.compute_great_circle_distance(
            self.a[0], self.a[1], self.a[0] + 0.055, self.a[1]
        )
        assert round(dist, 6) == round(6.115720965451057, 6)

    def test_south(self):
        dist = gis_utils.compute_great_circle_distance(
            self.a[0], self.a[1], self.a[0] - 0.055, self.a[1]
        )
        assert round(dist, 6) == round(6.115720965451057, 6)

    def test_east(self):
        dist = gis_utils.compute_great_circle_distance(
            self.a[0], self.a[1], self.a[0], self.a[1] + 0.055
        )
        assert round(dist, 6) == round(4.212136811327167, 6)

    def test_west(self):
        dist = gis_utils.compute_great_circle_distance(
            self.a[0], self.a[1], self.a[0], self.a[1] - 0.055
        )
        assert round(dist, 6) == round(4.212136811327167, 6)

    def test_north_east(self):
        dist = gis_utils.compute_great_circle_distance(
            self.a[0], self.a[1], self.a[0] + 0.055, self.a[1] + 0.055
        )
        assert round(dist, 6) == round(7.4247024128101895, 6)

    def test_south_east(self):
        dist = gis_utils.compute_great_circle_distance(
            self.a[0], self.a[1], self.a[0] - 0.055, self.a[1] + 0.055
        )
        assert round(dist, 6) == round(7.427116672788511, 6)

    def test_north_west(self):
        dist = gis_utils.compute_great_circle_distance(
            self.a[0], self.a[1], self.a[0] + 0.055, self.a[1] - 0.055
        )
        assert round(dist, 6) == round(7.4247024128101895, 6)

    def test_south_west(self):
        dist = gis_utils.compute_great_circle_distance(
            self.a[0], self.a[1], self.a[0] - 0.055, self.a[1] - 0.055
        )
        assert round(dist, 6) == round(7.427116672788511, 6)


class TestComputeEuclideanDistance:
    def setup_method(self):
        self.a = (46.46961, 10.36953)  # Bormio.

    def test_example_from_wikipedia(self):
        # Src: https://en.wikipedia.org/wiki/Haversine_formula#Example
        white_house = (38.898, -77.037)
        eiffel_tower = (48.858, 2.294)
        args = white_house[0], white_house[1], eiffel_tower[0], eiffel_tower[1]

        dist = gis_utils.compute_euclidean_distance(*args)
        dist_actual = gis_utils.compute_great_circle_distance(*args)
        assert (dist - dist_actual) * 100 / dist_actual < 5  # Error: <5%.

    def test_example_from_scikit(self):
        # Src: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.haversine_distances.html
        bsas = (-34.83333, -58.5166646)  # Ezeiza Airport (Buenos Aires, Argentina).
        paris = (49.0083899664, 2.53844117956)  # C. de Gaulle Airport (Paris, France).
        args = bsas[0], bsas[1], paris[0], paris[1]

        dist = gis_utils.compute_euclidean_distance(*args)
        dist_actual = gis_utils.compute_great_circle_distance(*args)
        assert (dist - dist_actual) * 100 / dist_actual < 4  # Error: <4%.

    def test_example_from_geopy(self):
        # Src: https://github.com/geopy/geopy?tab=readme-ov-file#measuring-distance
        newport_ri = (41.49008, -71.312796)
        cleveland_oh = (41.499498, -81.695391)
        args = newport_ri[0], newport_ri[1], cleveland_oh[0], cleveland_oh[1]

        dist = gis_utils.compute_euclidean_distance(*args)
        dist_actual = gis_utils.compute_great_circle_distance(*args)
        assert (dist - dist_actual) * 100 / dist_actual < 0.5  # Error: <0.5%.

    def test_north(self):
        args = self.a[0], self.a[1], self.a[0] + 0.055, self.a[1]
        dist = gis_utils.compute_euclidean_distance(*args)
        dist_actual = gis_utils.compute_great_circle_distance(*args)
        assert round(dist, 5) == round(dist_actual, 5)

    def test_south(self):
        args = self.a[0], self.a[1], self.a[0] - 0.055, self.a[1]
        dist = gis_utils.compute_euclidean_distance(*args)
        dist_actual = gis_utils.compute_great_circle_distance(*args)
        assert round(dist, 5) == round(dist_actual, 5)

    def test_east(self):
        args = self.a[0], self.a[1], self.a[0], self.a[1] + 0.055
        dist = gis_utils.compute_euclidean_distance(*args)
        dist_actual = gis_utils.compute_great_circle_distance(*args)
        assert round(dist, 5) == round(dist_actual, 5)

    def test_west(self):
        args = self.a[0], self.a[1], self.a[0], self.a[1] - 0.055
        dist = gis_utils.compute_euclidean_distance(*args)
        dist_actual = gis_utils.compute_great_circle_distance(*args)
        assert round(dist, 5) == round(dist_actual, 5)

    def test_north_east(self):
        args = self.a[0], self.a[1], self.a[0] + 0.055, self.a[1] + 0.055
        dist = gis_utils.compute_euclidean_distance(*args)
        dist_actual = gis_utils.compute_great_circle_distance(*args)
        assert round(dist, 5) == round(dist_actual, 5)

    def test_south_east(self):
        args = self.a[0], self.a[1], self.a[0] - 0.055, self.a[1] + 0.055
        dist = gis_utils.compute_euclidean_distance(*args)
        dist_actual = gis_utils.compute_great_circle_distance(*args)
        assert round(dist, 5) == round(dist_actual, 5)

    def test_north_west(self):
        args = self.a[0], self.a[1], self.a[0] + 0.055, self.a[1] - 0.055
        dist = gis_utils.compute_euclidean_distance(*args)
        dist_actual = gis_utils.compute_great_circle_distance(*args)
        assert round(dist, 5) == round(dist_actual, 5)

    def test_south_west(self):
        args = self.a[0], self.a[1], self.a[0] - 0.055, self.a[1] - 0.055
        dist = gis_utils.compute_euclidean_distance(*args)
        dist_actual = gis_utils.compute_great_circle_distance(*args)
        assert round(dist, 5) == round(dist_actual, 5)
