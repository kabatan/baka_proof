import MathAutoResearch.GeometryFull2D.RuleLemmas

namespace MathAutoResearch.GeometryFull2D

theorem v06_sealed_holdout_0000
    (P01 P02 P03 P04 P05 P11 P12 P17 P19 P22 P23 P28 : Point)
    (L18 L26 : Line)
    (C10 C27 C28 : Circle)
    (h00 : circle_with_center_through_point P28 P17 C27)
    (h01 : directed_angle_eq_mod_pi P02 P23 P12 P01 P22 P11)
    (h02 : midpoint P05 P04 P03)
    (h03 : line_circle_intersection P03 L18 C10)
    (h04 : line_circle_intersection P19 L26 C28)
    : on_circle P17 C27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0000
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0000

theorem v06_sealed_holdout_0001
    (P00 P03 P05 P09 P12 P13 P14 P17 P19 P21 P23 P28 P29 : Point)
    (L02 L26 : Line)
    (C06 C20 C23 : Circle)
    (h00 : circle_through_three_noncollinear_points P17 P21 P29 C23)
    (h01 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h02 : midpoint P12 P13 P14)
    (h03 : line_circle_intersection P19 L26 C20)
    (h04 : line_circle_intersection P03 L02 C06)
    : on_circle P17 C23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0001
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0001

theorem v06_sealed_holdout_0002
    (P02 P03 P07 P09 P12 P16 P19 P21 P22 P25 P30 : Point)
    (L21 : Line)
    (C27 : Circle)
    (h00 : line_circle_intersection P22 L21 C27)
    (h01 : between P16 P09 P02)
    (h02 : midpoint P19 P22 P25)
    (h03 : midpoint P22 P03 P16)
    (h04 : area_le P25 P16 P07 P30 P21 P12)
    : on_circle P22 C27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0002
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0002

theorem v06_sealed_holdout_0003
    (P03 P04 P09 P12 P14 P17 P19 P26 P27 P29 P31 : Point)
    (L18 L26 : Line)
    (C04 C20 C26 : Circle)
    (h00 : chord P19 P17 C20)
    (h01 : line_circle_intersection P19 L26 C04)
    (h02 : area_le P26 P31 P04 P09 P14 P19)
    (h03 : midpoint P29 P12 P27)
    (h04 : line_circle_intersection P03 L18 C26)
    : on_circle P19 C20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0003
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0003

theorem v06_sealed_holdout_0004
    (P02 P04 P05 P15 P24 P25 P26 P27 P28 P30 P31 : Point)
    (L12 L16 L20 L30 : Line)
    (C02 : Circle)
    (h00 : tangent_chord_angle P28 P24 P25 L30 C02)
    (h01 : between P30 P27 P24)
    (h02 : angle_bisector_line P26 P30 P15 P27 L20)
    (h03 : angle_bisector_line P31 P02 P15 P27 L16)
    (h04 : angle_bisector_line P04 P05 P15 P27 L12)
    : on_circle P25 C02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0004
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0004

theorem v06_sealed_holdout_0005
    (P00 P01 P02 P03 P04 P05 P08 P10 P11 P12 P14 P17 P21 P23 P26 P30 P31 : Point)
    (L19 : Line)
    (C04 : Circle)
    (h00 : line_circle_intersection P05 L19 C04)
    (h01 : area_le P05 P04 P03 P02 P01 P00)
    (h02 : directed_angle_eq_mod_pi P08 P17 P26 P03 P12 P21)
    (h03 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h04 : area_le P14 P11 P08 P05 P02 P31)
    : on_line P05 L19 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0005
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0005

theorem v06_sealed_holdout_0006
    (P03 P11 P15 P19 P23 P26 P27 P28 P30 : Point)
    (L10 L11 L12 L18 : Line)
    (C02 C10 C18 C24 : Circle)
    (h00 : altitude P26 P03 P11 P23 L11)
    (h01 : line_circle_intersection P03 L18 C02)
    (h02 : angle_bisector_line P28 P30 P15 P27 L12)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : line_circle_intersection P19 L10 C24)
    : on_line P11 L11 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0006
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0006

theorem v06_sealed_holdout_0007
    (P02 P03 P05 P07 P10 P15 P16 P17 P19 P22 P23 P25 P27 P28 P29 P31 : Point)
    (L12 L16 : Line)
    (h00 : angle_bisector_line P15 P07 P17 P29 L12)
    (h01 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    (h02 : area_le P22 P03 P16 P29 P10 P23)
    (h03 : between P25 P16 P07)
    (h04 : angle_bisector_line P07 P05 P15 P27 L16)
    : on_line P15 L12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0007
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0007

theorem v06_sealed_holdout_0008
    (P00 P03 P04 P08 P10 P11 P12 P18 P19 P25 P27 P29 : Point)
    (L00 L02 L26 : Line)
    (C12 C22 C28 : Circle)
    (h00 : line_circle_intersection P08 L00 C28)
    (h01 : line_circle_intersection P03 L02 C22)
    (h02 : area_le P29 P12 P27 P10 P25 P08)
    (h03 : area_le P00 P25 P18 P11 P04 P29)
    (h04 : line_circle_intersection P19 L26 C12)
    : on_line P08 L00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0008
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0008

theorem v06_sealed_holdout_0009
    (P01 P02 P03 P04 P07 P08 P10 P14 P15 P19 P20 P21 P22 P24 P25 P28 P29 P30 P31 : Point)
    (L18 : Line)
    (C18 : Circle)
    (h00 : equilateral P21 P28 P31)
    (h01 : area_le P01 P08 P15 P22 P29 P04)
    (h02 : line_circle_intersection P03 L18 C18)
    (h03 : directed_angle_eq_mod_pi P07 P02 P29 P24 P19 P14)
    (h04 : area_le P10 P15 P20 P25 P30 P03)
    : equal_length P21 P28 P28 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0009
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0009

theorem v06_sealed_holdout_0010
    (P04 P08 P09 P10 P11 P12 P13 P14 P16 P17 P19 P23 P26 P29 P30 : Point)
    (C02 C22 : Circle)
    (h00 : length_sum P26 P14 P29 P09 P16 P23)
    (h01 : directed_angle_eq_mod_pi P13 P12 P11 P10 P09 P08)
    (h02 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h03 : between P14 P11 P08)
    (h04 : circle_circle_intersection P19 C22 C02)
    : length_sum P29 P09 P26 P14 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0010
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0010

theorem v06_sealed_holdout_0011
    (P03 P05 P15 P16 P17 P18 P19 P20 P21 P23 P24 P27 P31 : Point)
    (L07 : Line)
    (C02 C18 C23 : Circle)
    (h00 : equal_length P23 P24 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : line_circle_intersection P31 L07 C23)
    (h03 : area_le P21 P20 P19 P18 P17 P16)
    (h04 : circle_circle_intersection P03 C02 C18)
    : equal_length P23 P24 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0011
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0011

theorem v06_sealed_holdout_0012
    (P00 P01 P02 P05 P11 P12 P13 P14 P15 P21 P23 P24 P27 P28 P29 P30 P31 : Point)
    (L12 : Line)
    (C22 C26 : Circle)
    (h00 : area_eq P12 P28 P21 P01 P13 P23)
    (h01 : area_eq P01 P13 P23 P02 P14 P24)
    (h02 : circle_circle_intersection P11 C22 C26)
    (h03 : area_le P28 P29 P30 P31 P00 P01)
    (h04 : angle_bisector_line P12 P05 P15 P27 L12)
    : area_eq P12 P28 P21 P02 P14 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0012
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0012

theorem v06_sealed_holdout_0013
    (P02 P05 P06 P08 P13 P15 P16 P24 P25 P27 P30 : Point)
    (L24 L28 : Line)
    (h00 : equal_length P25 P24 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : angle_bisector_line P25 P06 P30 P13 L28)
    (h03 : angle_bisector_line P08 P02 P15 P27 L28)
    (h04 : angle_bisector_line P13 P05 P15 P27 L24)
    : equal_length P25 P24 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0013
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0013

theorem v06_sealed_holdout_0014
    (P02 P04 P05 P06 P07 P10 P14 P15 P20 P21 P25 P26 P27 P29 : Point)
    (L02 L04 : Line)
    (C14 : Circle)
    (h00 : tangent_chord_angle P06 P25 P26 L02 C14)
    (h01 : midpoint P04 P21 P06)
    (h02 : midpoint P07 P02 P29)
    (h03 : between P10 P15 P20)
    (h04 : angle_bisector_line P14 P05 P15 P27 L04)
    : on_circle P26 C14 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0014
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0014

theorem v06_sealed_holdout_0015
    (P00 P03 P05 P10 P11 P15 P16 P17 P23 P24 P27 P28 P31 : Point)
    (L16 L24 L28 : Line)
    (h00 : angle_bisector_line P11 P10 P23 P03 L24)
    (h01 : angle_bisector_line P00 P28 P15 P27 L28)
    (h02 : angle_bisector_line P05 P31 P15 P27 L24)
    (h03 : midpoint P17 P24 P31)
    (h04 : angle_bisector_line P15 P05 P16 P27 L16)
    : angle_bisector P11 P10 P23 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0015
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0015

theorem v06_sealed_holdout_0016
    (P01 P03 P05 P06 P07 P10 P14 P15 P16 P17 P19 P20 P23 P24 P26 P27 P28 P31 : Point)
    (L04 : Line)
    (h00 : directed_angle_eq_mod_pi P20 P17 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : angle_bisector_line P06 P31 P15 P27 L04)
    (h03 : area_le P24 P01 P10 P19 P28 P05)
    (h04 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    : directed_angle_eq_mod_pi P20 P17 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0016
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0016

theorem v06_sealed_holdout_0017
    (P01 P02 P05 P07 P09 P10 P11 P12 P16 P18 P21 P22 P23 P24 P25 P30 P31 : Point)
    (h00 : directed_angle_eq_mod_2pi P09 P21 P10 P22 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P22 P30 P07 P16 P25 P02)
    (h02 : directed_angle_eq_mod_pi P30 P11 P24 P05 P18 P31)
    (h03 : between P31 P10 P21)
    (h04 : directed_angle_eq_mod_pi P02 P23 P12 P01 P22 P11)
    : directed_angle_eq_mod_2pi P09 P21 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0017
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0017

theorem v06_sealed_holdout_0018
    (P00 P03 P06 P07 P13 P15 P16 P17 P19 P22 P23 P24 P26 P31 : Point)
    (L10 : Line)
    (C02 C16 C30 : Circle)
    (h00 : directed_angle_eq_mod_pi P22 P17 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    (h04 : line_circle_intersection P19 L10 C16)
    : directed_angle_eq_mod_pi P22 P17 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0018
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0018

theorem v06_sealed_holdout_0019
    (P02 P07 P09 P11 P16 P19 P21 P22 P25 P30 P31 : Point)
    (C02 C06 C14 C15 : Circle)
    (h00 : directed_angle_eq_mod_2pi P11 P21 P09 P22 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P22 P30 P07 P16 P25 P02)
    (h02 : circle_circle_intersection P31 C14 C15)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : between P16 P09 P02)
    : directed_angle_eq_mod_2pi P11 P21 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0019
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0019

theorem v06_sealed_holdout_0020
    (P00 P01 P02 P03 P08 P13 P15 P16 P17 P18 P23 P24 P27 P30 P31 : Point)
    (L16 : Line)
    (C18 C26 C27 : Circle)
    (h00 : circle_through_three_noncollinear_points P00 P01 P15 C27)
    (h01 : circle_circle_intersection P03 C26 C18)
    (h02 : between P17 P24 P31)
    (h03 : angle_bisector_line P15 P02 P16 P27 L16)
    (h04 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    : triangle_pred P00 P01 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0020
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0020

theorem v06_sealed_holdout_0021
    (P00 P03 P05 P15 P18 P19 P21 P24 P27 P30 : Point)
    (L26 : Line)
    (C02 C06 C18 C28 : Circle)
    (h00 : equilateral P21 P00 P05)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : line_circle_intersection P19 L26 C28)
    (h04 : area_le P30 P27 P24 P21 P18 P15)
    : triangle_pred P21 P00 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0021
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0021

theorem v06_sealed_holdout_0022
    (P00 P01 P02 P11 P12 P15 P19 P22 P23 P27 P28 P29 P30 P31 : Point)
    (L12 : Line)
    (C02 C06 C09 : Circle)
    (h00 : circle_through_three_noncollinear_points P02 P00 P15 C09)
    (h01 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    (h02 : angle_bisector_line P12 P31 P15 P27 L12)
    (h03 : directed_angle_eq_mod_pi P02 P23 P12 P01 P22 P11)
    (h04 : circle_circle_intersection P19 C06 C02)
    : triangle_pred P02 P00 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0022
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0022

theorem v06_sealed_holdout_0023
    (P00 P03 P05 P06 P09 P14 P19 P23 P28 : Point)
    (L26 : Line)
    (C12 C18 C19 : Circle)
    (h00 : equilateral P23 P00 P05)
    (h01 : line_circle_intersection P19 L26 C12)
    (h02 : midpoint P06 P19 P00)
    (h03 : area_le P09 P00 P23 P14 P05 P28)
    (h04 : circle_circle_intersection P03 C18 C19)
    : triangle_pred P23 P00 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0023
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0023

theorem v06_sealed_holdout_0024
    (P00 P02 P03 P05 P09 P13 P16 P19 P20 P24 P27 : Point)
    (L10 L26 : Line)
    (C08 C10 C12 C18 : Circle)
    (h00 : equilateral P24 P00 P05)
    (h01 : circle_circle_intersection P03 C10 C18)
    (h02 : line_circle_intersection P19 L10 C08)
    (h03 : area_le P16 P09 P02 P27 P20 P13)
    (h04 : line_circle_intersection P19 L26 C12)
    : triangle_pred P24 P00 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0024
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0024

theorem v06_sealed_holdout_0025
    (P04 P05 P07 P09 P19 P20 P22 P24 P26 P31 : Point)
    (L25 L26 : Line)
    (C02 C04 C05 C22 : Circle)
    (RF28 : Reflection)
    (h00 : line_circle_intersection P07 L25 C05)
    (h01 : circle_circle_intersection P19 C22 C02)
    (h02 : directed_angle_eq_mod_pi P20 P05 P22 P07 P24 P09)
    (h03 : line_circle_intersection P19 L26 C04)
    (h04 : between P26 P31 P04)
    : reflection_image RF28 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0025
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0025

theorem v06_sealed_holdout_0026
    (P01 P03 P05 P14 P15 P19 P26 P27 : Point)
    (L18 L20 : Line)
    (C02 C06 C10 C18 C26 : Circle)
    (HOM49 : Homothety)
    (h00 : circle_circle_intersection P19 C06 C02)
    (h01 : line_circle_intersection P03 L18 C10)
    (h02 : midpoint P27 P14 P01)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : angle_bisector_line P26 P05 P15 P27 L20)
    : homothety_image HOM49 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0026
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0026

theorem v06_sealed_holdout_0027
    (P00 P02 P03 P06 P07 P10 P11 P13 P15 P21 P22 P27 P30 P31 : Point)
    (L02 L04 L12 : Line)
    (C02 C06 C18 : Circle)
    (INV10 : Inversion)
    (h00 : angle_bisector_line P07 P06 P30 P13 L12)
    (h01 : area_le P31 P10 P21 P00 P11 P22)
    (h02 : line_circle_intersection P03 L02 C06)
    (h03 : angle_bisector_line P22 P02 P15 P27 L04)
    (h04 : circle_circle_intersection P03 C02 C18)
    : inversion_image INV10 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0027
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0027

theorem v06_sealed_holdout_0028
    (P00 P05 P06 P07 P09 P11 P12 P13 P14 P15 P16 P17 P19 P23 P26 P27 : Point)
    (SP39 : SpiralSimilarity)
    (h00 : midpoint P11 P14 P17)
    (h01 : area_le P06 P19 P00 P13 P26 P07)
    (h02 : midpoint P09 P00 P23)
    (h03 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h04 : directed_angle_eq_mod_pi P15 P26 P05 P16 P27 P06)
    : spiral_similarity_center SP39 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0028
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0028

theorem v06_sealed_holdout_0029
    (P00 P03 P08 P17 P18 P19 P23 P27 P28 P31 : Point)
    (C18 C26 : Circle)
    (h00 : P17 = P08)
    (h01 : P00 = P19)
    (h02 : P27 = P31)
    (h03 : between P18 P23 P28)
    (h04 : circle_circle_intersection P03 C26 C18)
    : rotation_preserves_collinear P17 P00 P27 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0029
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0029

theorem v06_sealed_holdout_0030
    (P04 P05 P06 P09 P13 P14 P15 P18 P19 P20 P22 P23 P26 P27 P30 P31 : Point)
    (L04 : Line)
    (C31 : Circle)
    (h00 : circle_with_center_through_point P26 P18 C31)
    (h01 : between P20 P05 P22)
    (h02 : midpoint P23 P18 P13)
    (h03 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    (h04 : angle_bisector_line P30 P06 P15 P27 L04)
    : on_circle P18 C31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0030
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0030

theorem v06_sealed_holdout_0031
    (P01 P04 P06 P08 P14 P15 P18 P19 P21 P22 P23 P24 P25 P27 P29 P30 : Point)
    (C02 C22 C25 : Circle)
    (h00 : circle_through_three_noncollinear_points P15 P22 P29 C25)
    (h01 : midpoint P27 P14 P01)
    (h02 : area_le P30 P27 P24 P21 P18 P15)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : area_le P04 P21 P06 P23 P08 P25)
    : on_circle P15 C25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0031
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0031

theorem v06_sealed_holdout_0032
    (P00 P01 P02 P03 P04 P05 P08 P11 P12 P17 P20 P21 P23 P26 P30 : Point)
    (L21 : Line)
    (C09 : Circle)
    (h00 : line_circle_intersection P20 L21 C09)
    (h01 : between P02 P23 P12)
    (h02 : area_le P05 P04 P03 P02 P01 P00)
    (h03 : directed_angle_eq_mod_pi P08 P17 P26 P03 P12 P21)
    (h04 : between P11 P30 P17)
    : on_circle P20 C09 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0032
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0032

theorem v06_sealed_holdout_0033
    (P00 P01 P02 P06 P09 P12 P13 P14 P15 P16 P17 P18 P23 P27 P28 : Point)
    (L08 L12 : Line)
    (C28 : Circle)
    (h00 : chord P17 P18 C28)
    (h01 : between P09 P00 P23)
    (h02 : area_le P12 P13 P14 P15 P16 P17)
    (h03 : angle_bisector_line P28 P02 P15 P27 L12)
    (h04 : angle_bisector_line P01 P06 P15 P27 L08)
    : on_circle P17 C28 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0033
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0033

theorem v06_sealed_holdout_0034
    (P02 P03 P09 P10 P16 P19 P22 P23 P25 P26 P27 P29 : Point)
    (L10 : Line)
    (C02 C06 C22 C30 : Circle)
    (h00 : tangent_chord_angle P26 P25 P27 L10 C06)
    (h01 : midpoint P16 P09 P02)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : area_le P22 P03 P16 P29 P10 P23)
    (h04 : circle_circle_intersection P19 C22 C02)
    : on_circle P27 C06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0034
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0034

theorem v06_sealed_holdout_0035
    (P03 P04 P06 P08 P09 P10 P12 P14 P15 P19 P25 P26 P27 P29 P31 : Point)
    (L00 L21 : Line)
    (C02 C14 C20 : Circle)
    (h00 : line_circle_intersection P03 L21 C20)
    (h01 : circle_circle_intersection P19 C14 C02)
    (h02 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    (h03 : directed_angle_eq_mod_pi P29 P12 P27 P10 P25 P08)
    (h04 : angle_bisector_line P03 P06 P15 P27 L00)
    : on_line P03 L21 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0035
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0035

theorem v06_sealed_holdout_0036
    (P01 P04 P06 P08 P11 P15 P19 P21 P23 P24 P25 P27 P30 : Point)
    (L17 L26 : Line)
    (C04 : Circle)
    (h00 : altitude P24 P04 P11 P23 L17)
    (h01 : between P30 P27 P24)
    (h02 : midpoint P01 P08 P15)
    (h03 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    (h04 : line_circle_intersection P19 L26 C04)
    : on_line P11 L17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0036
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0036

theorem v06_sealed_holdout_0037
    (P03 P04 P05 P06 P07 P10 P11 P13 P15 P17 P23 P27 P29 P30 : Point)
    (L16 L24 : Line)
    (C02 C18 : Circle)
    (h00 : angle_bisector_line P13 P07 P17 P29 L16)
    (h01 : between P05 P04 P03)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : area_le P11 P30 P17 P04 P23 P10)
    (h04 : angle_bisector_line P05 P06 P15 P27 L24)
    : on_line P13 L16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0037
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0037

theorem v06_sealed_holdout_0038
    (P03 P05 P06 P15 P16 P19 P26 P27 : Point)
    (L02 L10 L18 : Line)
    (C02 C06 C12 C24 : Circle)
    (h00 : line_circle_intersection P06 L02 C12)
    (h01 : line_circle_intersection P03 L18 C02)
    (h02 : area_le P15 P26 P05 P16 P27 P06)
    (h03 : line_circle_intersection P03 L02 C06)
    (h04 : line_circle_intersection P19 L10 C24)
    : on_line P06 L02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0038
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0038

theorem v06_sealed_holdout_0039
    (P03 P07 P16 P19 P22 P25 P29 P31 : Point)
    (L18 : Line)
    (C02 C18 C26 : Circle)
    (h00 : equilateral P19 P29 P31)
    (h01 : between P19 P22 P25)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : midpoint P25 P16 P07)
    (h04 : line_circle_intersection P03 L18 C02)
    : equal_length P19 P29 P29 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0039
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0039

theorem v06_sealed_holdout_0040
    (P00 P09 P15 P16 P18 P19 P23 P24 P25 P27 P29 : Point)
    (L10 : Line)
    (C02 C08 C10 C22 C30 : Circle)
    (h00 : length_sum P24 P15 P29 P09 P16 P23)
    (h01 : circle_circle_intersection P27 C22 C10)
    (h02 : line_circle_intersection P19 L10 C08)
    (h03 : midpoint P00 P25 P18)
    (h04 : circle_circle_intersection P19 C30 C02)
    : length_sum P29 P09 P24 P15 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0040
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0040

theorem v06_sealed_holdout_0041
    (P02 P03 P05 P07 P10 P13 P14 P15 P16 P19 P20 P21 P24 P25 P27 P29 P30 P31 : Point)
    (L28 : Line)
    (h00 : equal_length P21 P25 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : angle_bisector_line P21 P07 P31 P13 L28)
    (h03 : area_le P07 P02 P29 P24 P19 P14)
    (h04 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    : equal_length P21 P25 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0041
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0041

theorem v06_sealed_holdout_0042
    (P01 P02 P06 P08 P10 P11 P12 P13 P14 P17 P20 P21 P23 P24 P29 P31 : Point)
    (h00 : area_eq P10 P29 P21 P01 P12 P23)
    (h01 : area_eq P01 P12 P23 P02 P13 P24)
    (h02 : midpoint P13 P12 P11)
    (h03 : midpoint P14 P11 P08)
    (h04 : area_le P17 P24 P31 P06 P13 P20)
    : area_eq P10 P29 P21 P02 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0042
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0042

theorem v06_sealed_holdout_0043
    (P01 P05 P10 P15 P16 P19 P20 P21 P22 P23 P24 P25 P27 : Point)
    (h00 : equal_length P23 P25 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : between P20 P21 P22)
    (h03 : midpoint P21 P20 P19)
    (h04 : between P24 P01 P10)
    : equal_length P23 P25 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0043
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0043

theorem v06_sealed_holdout_0044
    (P03 P04 P07 P10 P12 P15 P16 P21 P22 P23 P25 P26 P27 P29 P30 P31 : Point)
    (L14 L16 : Line)
    (C18 : Circle)
    (h00 : tangent_chord_angle P04 P26 P25 L14 C18)
    (h01 : area_le P22 P03 P16 P29 P10 P23)
    (h02 : area_le P25 P16 P07 P30 P21 P12)
    (h03 : angle_bisector_line P07 P03 P15 P27 L16)
    (h04 : between P31 P10 P21)
    : on_circle P25 C18 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0044
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0044

theorem v06_sealed_holdout_0045
    (P03 P06 P09 P11 P12 P13 P15 P23 P27 P29 : Point)
    (L24 L26 : Line)
    (C02 C18 : Circle)
    (h00 : angle_bisector_line P09 P11 P23 P03 L26)
    (h01 : between P29 P12 P27)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : between P03 P06 P09)
    (h04 : angle_bisector_line P13 P06 P15 P27 L24)
    : angle_bisector P09 P11 P23 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0045
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0045

theorem v06_sealed_holdout_0046
    (P03 P06 P07 P14 P15 P16 P18 P19 P23 P24 P27 P31 : Point)
    (L02 L04 : Line)
    (C02 C14 C22 : Circle)
    (h00 : directed_angle_eq_mod_pi P18 P19 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : line_circle_intersection P03 L02 C22)
    (h04 : angle_bisector_line P14 P06 P15 P27 L04)
    : directed_angle_eq_mod_pi P18 P19 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0046
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0046

theorem v06_sealed_holdout_0047
    (P02 P05 P07 P08 P09 P15 P16 P19 P20 P21 P22 P25 P30 : Point)
    (L10 : Line)
    (C00 C14 C30 : Circle)
    (h00 : directed_angle_eq_mod_2pi P07 P22 P09 P21 P30 P08)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P08 P16 P25 P02)
    (h02 : circle_circle_intersection P15 C14 C30)
    (h03 : line_circle_intersection P19 L10 C00)
    (h04 : midpoint P20 P05 P22)
    : directed_angle_eq_mod_2pi P07 P22 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0047
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0047

theorem v06_sealed_holdout_0048
    (P00 P01 P03 P06 P07 P14 P15 P16 P18 P20 P23 P24 P26 P27 P31 : Point)
    (L04 L18 : Line)
    (C10 : Circle)
    (h00 : directed_angle_eq_mod_pi P20 P18 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : angle_bisector_line P06 P00 P15 P27 L04)
    (h03 : line_circle_intersection P03 L18 C10)
    (h04 : area_le P27 P14 P01 P20 P07 P26)
    : directed_angle_eq_mod_pi P20 P18 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0048
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0048

theorem v06_sealed_holdout_0049
    (P02 P06 P07 P09 P10 P11 P15 P16 P17 P19 P21 P22 P24 P25 P27 P30 : Point)
    (L08 L26 : Line)
    (C20 : Circle)
    (h00 : directed_angle_eq_mod_2pi P09 P22 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : midpoint P30 P11 P24)
    (h03 : line_circle_intersection P19 L26 C20)
    (h04 : angle_bisector_line P17 P06 P15 P27 L08)
    : directed_angle_eq_mod_2pi P09 P22 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0049
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0049

theorem v06_sealed_holdout_0050
    (P00 P01 P03 P06 P09 P15 P18 P19 P25 P27 P30 : Point)
    (L20 : Line)
    (C13 : Circle)
    (h00 : circle_through_three_noncollinear_points P30 P01 P15 C13)
    (h01 : midpoint P00 P25 P18)
    (h02 : midpoint P03 P06 P09)
    (h03 : midpoint P06 P19 P00)
    (h04 : angle_bisector_line P18 P06 P15 P27 L20)
    : triangle_pred P30 P01 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0050
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0050

theorem v06_sealed_holdout_0051
    (P01 P02 P03 P05 P07 P09 P13 P16 P19 P20 P27 P29 : Point)
    (L02 L10 : Line)
    (C08 C22 : Circle)
    (h00 : equilateral P19 P01 P05)
    (h01 : midpoint P07 P02 P29)
    (h02 : line_circle_intersection P03 L02 C22)
    (h03 : line_circle_intersection P19 L10 C08)
    (h04 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    : triangle_pred P19 P01 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0051
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0051

theorem v06_sealed_holdout_0052
    (P00 P03 P04 P06 P08 P13 P17 P18 P20 P23 P24 P25 P26 P30 P31 : Point)
    (C18 C19 : Circle)
    (h00 : equilateral P25 P00 P06)
    (h01 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    (h02 : circle_circle_intersection P03 C18 C19)
    (h03 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    (h04 : between P26 P31 P04)
    : triangle_pred P25 P00 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0052
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0052

theorem v06_sealed_holdout_0053
    (P01 P03 P05 P10 P15 P16 P17 P18 P19 P20 P21 P24 P27 P30 : Point)
    (L28 : Line)
    (h00 : equilateral P21 P01 P05)
    (h01 : area_le P21 P20 P19 P18 P17 P16)
    (h02 : midpoint P24 P01 P10)
    (h03 : angle_bisector_line P16 P03 P15 P27 L28)
    (h04 : midpoint P30 P27 P24)
    : triangle_pred P21 P01 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0053
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0053

theorem v06_sealed_holdout_0054
    (P00 P01 P02 P03 P04 P05 P10 P12 P21 P22 P23 P28 P29 P30 P31 : Point)
    (h00 : equilateral P22 P01 P05)
    (h01 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    (h02 : midpoint P31 P10 P21)
    (h03 : midpoint P02 P23 P12)
    (h04 : area_le P05 P04 P03 P02 P01 P00)
    : triangle_pred P22 P01 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0054
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0054

theorem v06_sealed_holdout_0055
    (P00 P03 P06 P07 P12 P13 P14 P19 P31 : Point)
    (L10 L12 : Line)
    (C02 C16 C30 : Circle)
    (RF46 : Reflection)
    (h00 : angle_bisector_line P03 P07 P31 P13 L12)
    (h01 : circle_circle_intersection P19 C30 C02)
    (h02 : midpoint P06 P19 P00)
    (h03 : line_circle_intersection P19 L10 C16)
    (h04 : midpoint P12 P13 P14)
    : reflection_image RF46 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0055
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0055

theorem v06_sealed_holdout_0056
    (P02 P03 P05 P09 P10 P11 P13 P15 P16 P19 P20 P24 P25 P26 P27 P28 P30 : Point)
    (L26 : Line)
    (C12 : Circle)
    (HOM63 : Homothety)
    (h00 : midpoint P15 P10 P05)
    (h01 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    (h02 : directed_angle_eq_mod_pi P13 P28 P11 P26 P09 P24)
    (h03 : area_le P16 P09 P02 P27 P20 P13)
    (h04 : line_circle_intersection P19 L26 C12)
    : homothety_image HOM63 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0056
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0056

theorem v06_sealed_holdout_0057
    (P03 P04 P13 P16 P17 P18 P19 P22 P23 P24 P26 P31 : Point)
    (L18 : Line)
    (C18 : Circle)
    (INV20 : Inversion)
    (h00 : between P22 P19 P16)
    (h01 : between P17 P24 P31)
    (h02 : line_circle_intersection P03 L18 C18)
    (h03 : between P23 P18 P13)
    (h04 : midpoint P26 P31 P04)
    : inversion_image INV20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0057
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0057

theorem v06_sealed_holdout_0058
    (P01 P03 P08 P15 P19 P24 P25 P26 P27 P28 P29 : Point)
    (L02 L18 : Line)
    (C02 C10 C14 C30 : Circle)
    (SP45 : SpiralSimilarity)
    (h00 : area_le P29 P28 P27 P26 P25 P24)
    (h01 : line_circle_intersection P03 L18 C10)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : line_circle_intersection P03 L02 C14)
    (h04 : midpoint P01 P08 P15)
    : spiral_similarity_center SP45 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0058
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0058

theorem v06_sealed_holdout_0059
    (P01 P03 P04 P05 P06 P07 P08 P09 P15 P19 P27 P31 : Point)
    (L18 : Line)
    (C10 : Circle)
    (h00 : P15 = P08)
    (h01 : P01 = P19)
    (h02 : P27 = P31)
    (h03 : directed_angle_eq_mod_pi P04 P05 P06 P07 P08 P09)
    (h04 : line_circle_intersection P03 L18 C10)
    : rotation_preserves_collinear P15 P01 P27 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0059
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0059

theorem v06_sealed_holdout_0060
    (P00 P05 P06 P07 P09 P12 P13 P14 P15 P16 P17 P19 P23 P24 P26 P27 P28 : Point)
    (L12 : Line)
    (C03 : Circle)
    (h00 : circle_with_center_through_point P24 P19 C03)
    (h01 : area_le P06 P19 P00 P13 P26 P07)
    (h02 : area_le P09 P00 P23 P14 P05 P28)
    (h03 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h04 : angle_bisector_line P28 P06 P15 P27 L12)
    : on_circle P19 C03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0060
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0060

theorem v06_sealed_holdout_0061
    (P03 P10 P11 P13 P16 P19 P22 P23 P28 P29 : Point)
    (L18 : Line)
    (C02 C26 C27 C30 : Circle)
    (h00 : circle_through_three_noncollinear_points P13 P23 P29 C27)
    (h01 : between P13 P28 P11)
    (h02 : line_circle_intersection P03 L18 C26)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    : on_circle P13 C27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0061
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0061

theorem v06_sealed_holdout_0062
    (P03 P05 P08 P12 P13 P18 P20 P22 P23 P27 P29 P30 : Point)
    (L02 L21 : Line)
    (C22 C23 : Circle)
    (h00 : line_circle_intersection P18 L21 C23)
    (h01 : between P20 P05 P22)
    (h02 : area_le P23 P18 P13 P08 P03 P30)
    (h03 : line_circle_intersection P03 L02 C22)
    (h04 : between P29 P12 P27)
    : on_circle P18 C23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0062
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0062

theorem v06_sealed_holdout_0063
    (P01 P03 P04 P06 P07 P08 P14 P15 P19 P20 P21 P22 P23 P25 P26 P27 P29 : Point)
    (L02 : Line)
    (C04 C14 : Circle)
    (h00 : chord P15 P19 C04)
    (h01 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    (h02 : line_circle_intersection P03 L02 C14)
    (h03 : directed_angle_eq_mod_pi P01 P08 P15 P22 P29 P04)
    (h04 : area_le P04 P21 P06 P23 P08 P25)
    : on_circle P15 C04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0063
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0063

theorem v06_sealed_holdout_0064
    (P03 P04 P05 P15 P19 P24 P25 P26 P27 P28 : Point)
    (L00 L22 L26 : Line)
    (C10 C18 C28 : Circle)
    (h00 : tangent_chord_angle P24 P26 P25 L22 C10)
    (h01 : circle_circle_intersection P03 C10 C18)
    (h02 : midpoint P05 P04 P03)
    (h03 : angle_bisector_line P27 P03 P15 P28 L00)
    (h04 : line_circle_intersection P19 L26 C28)
    : on_circle P25 C10 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0064
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0064

theorem v06_sealed_holdout_0065
    (P00 P01 P05 P07 P09 P12 P13 P14 P16 P19 P23 P27 P28 : Point)
    (L08 L23 L26 : Line)
    (C04 C20 : Circle)
    (h00 : line_circle_intersection P01 L23 C04)
    (h01 : area_le P09 P00 P23 P14 P05 P28)
    (h02 : midpoint P12 P13 P14)
    (h03 : line_circle_intersection P19 L26 C20)
    (h04 : angle_bisector_line P01 P07 P16 P27 L08)
    : on_line P01 L23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0065
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0065

theorem v06_sealed_holdout_0066
    (P00 P02 P03 P05 P07 P09 P10 P11 P13 P15 P16 P20 P22 P23 P24 P27 P29 : Point)
    (L20 L23 L28 : Line)
    (h00 : altitude P22 P05 P11 P23 L23)
    (h01 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    (h02 : angle_bisector_line P24 P00 P15 P27 L28)
    (h03 : area_le P22 P03 P16 P29 P10 P23)
    (h04 : angle_bisector_line P02 P07 P16 P27 L20)
    : on_line P11 L23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0066
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0066

theorem v06_sealed_holdout_0067
    (P03 P04 P08 P11 P13 P17 P18 P19 P23 P26 P29 P31 : Point)
    (L10 L20 : Line)
    (C02 C08 C18 : Circle)
    (h00 : angle_bisector_line P11 P08 P17 P29 L20)
    (h01 : midpoint P23 P18 P13)
    (h02 : midpoint P26 P31 P04)
    (h03 : line_circle_intersection P19 L10 C08)
    (h04 : circle_circle_intersection P03 C02 C18)
    : on_line P11 L20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0067
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0067

theorem v06_sealed_holdout_0068
    (P01 P02 P03 P04 P07 P08 P14 P15 P18 P19 P21 P22 P24 P27 P29 P30 : Point)
    (L04 : Line)
    (C18 C19 C28 : Circle)
    (h00 : line_circle_intersection P04 L04 C28)
    (h01 : area_le P30 P27 P24 P21 P18 P15)
    (h02 : area_le P01 P08 P15 P22 P29 P04)
    (h03 : circle_circle_intersection P03 C18 C19)
    (h04 : area_le P07 P02 P29 P24 P19 P14)
    : on_line P04 L04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0068
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0068

theorem v06_sealed_holdout_0069
    (P00 P01 P02 P03 P04 P05 P08 P10 P11 P14 P17 P23 P30 P31 : Point)
    (C02 C18 : Circle)
    (h00 : equilateral P17 P30 P31)
    (h01 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h04 : midpoint P14 P11 P08)
    : equal_length P17 P30 P30 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0069
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0069

theorem v06_sealed_holdout_0070
    (P05 P06 P07 P08 P09 P15 P16 P17 P18 P19 P20 P21 P22 P23 P26 P27 P28 P29 P31 : Point)
    (h00 : length_sum P22 P16 P29 P09 P17 P23)
    (h01 : midpoint P17 P08 P31)
    (h02 : midpoint P15 P26 P05)
    (h03 : area_le P18 P07 P28 P17 P06 P27)
    (h04 : midpoint P21 P20 P19)
    : length_sum P29 P09 P22 P16 P17 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0070
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0070

theorem v06_sealed_holdout_0071
    (P05 P07 P08 P10 P15 P16 P17 P19 P24 P26 P27 : Point)
    (L10 L16 : Line)
    (C16 : Circle)
    (h00 : equal_length P19 P26 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : between P24 P17 P10)
    (h03 : line_circle_intersection P19 L10 C16)
    (h04 : angle_bisector_line P07 P08 P16 P27 L16)
    : equal_length P19 P26 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0071
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0071

theorem v06_sealed_holdout_0072
    (P01 P02 P03 P04 P06 P08 P09 P11 P12 P13 P15 P16 P18 P21 P23 P24 P26 P27 P30 P31 : Point)
    (L00 : Line)
    (h00 : area_eq P08 P30 P21 P01 P12 P23)
    (h01 : area_eq P01 P12 P23 P02 P13 P24)
    (h02 : area_le P31 P26 P21 P16 P11 P06)
    (h03 : angle_bisector_line P03 P04 P15 P27 L00)
    (h04 : area_le P03 P06 P09 P12 P15 P18)
    : area_eq P08 P30 P21 P02 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0072
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0072

theorem v06_sealed_holdout_0073
    (P00 P02 P03 P05 P06 P07 P15 P16 P21 P23 P26 P27 P29 : Point)
    (L02 : Line)
    (C22 : Circle)
    (h00 : equal_length P21 P26 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : directed_angle_eq_mod_pi P06 P03 P00 P29 P26 P23)
    (h03 : between P07 P02 P29)
    (h04 : line_circle_intersection P03 L02 C22)
    : equal_length P21 P26 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0073
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0073

theorem v06_sealed_holdout_0074
    (P00 P01 P02 P03 P08 P12 P15 P17 P19 P21 P25 P26 P27 : Point)
    (L10 L26 L28 : Line)
    (C00 C18 C22 C26 : Circle)
    (h00 : tangent_chord_angle P02 P27 P25 L26 C22)
    (h01 : area_le P08 P17 P26 P03 P12 P21)
    (h02 : angle_bisector_line P00 P01 P15 P27 L28)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : line_circle_intersection P19 L10 C00)
    : on_circle P25 C22 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0074
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0074

theorem v06_sealed_holdout_0075
    (P01 P03 P05 P06 P07 P10 P12 P15 P16 P17 P18 P19 P20 P21 P23 P24 P26 P27 P28 : Point)
    (L28 : Line)
    (h00 : angle_bisector_line P07 P12 P23 P03 L28)
    (h01 : directed_angle_eq_mod_pi P15 P26 P05 P16 P27 P06)
    (h02 : between P18 P07 P28)
    (h03 : area_le P21 P20 P19 P18 P17 P16)
    (h04 : midpoint P24 P01 P10)
    : angle_bisector P07 P12 P23 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0075
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0075

theorem v06_sealed_holdout_0076
    (P00 P01 P03 P07 P10 P15 P16 P17 P19 P21 P23 P24 P28 P29 P30 P31 : Point)
    (L10 : Line)
    (C16 : Circle)
    (h00 : directed_angle_eq_mod_pi P16 P19 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P17 P24)
    (h02 : line_circle_intersection P19 L10 C16)
    (h03 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    (h04 : between P31 P10 P21)
    : directed_angle_eq_mod_pi P16 P19 P03 P07 P17 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0076
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0076

theorem v06_sealed_holdout_0077
    (P00 P02 P04 P05 P06 P07 P08 P09 P12 P15 P16 P19 P21 P23 P25 P27 P30 : Point)
    (L28 : Line)
    (h00 : directed_angle_eq_mod_2pi P05 P23 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : midpoint P02 P07 P12)
    (h03 : angle_bisector_line P08 P04 P15 P27 L28)
    (h04 : between P06 P19 P00)
    : directed_angle_eq_mod_2pi P05 P23 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0077
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0077

theorem v06_sealed_holdout_0078
    (P02 P06 P07 P09 P10 P11 P13 P16 P19 P21 P22 P24 P25 P26 P27 P28 P30 P31 : Point)
    (L00 L31 : Line)
    (C31 : Circle)
    (h00 : directed_angle_eq_mod_2pi P11 P22 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : line_circle_intersection P31 L31 C31)
    (h03 : area_le P13 P28 P11 P26 P09 P24)
    (h04 : angle_bisector_line P19 P06 P16 P27 L00)
    : directed_angle_eq_mod_2pi P11 P22 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0078
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0078

theorem v06_sealed_holdout_0079
    (P02 P04 P07 P08 P09 P10 P11 P15 P16 P20 P21 P23 P25 P27 P29 P30 : Point)
    (L16 L20 : Line)
    (h00 : directed_angle_eq_mod_2pi P07 P23 P09 P21 P30 P08)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P08 P16 P25 P02)
    (h02 : area_le P16 P25 P02 P11 P20 P29)
    (h03 : angle_bisector_line P10 P04 P15 P27 L20)
    (h04 : angle_bisector_line P15 P07 P16 P27 L16)
    : directed_angle_eq_mod_2pi P07 P23 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0079
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0079

theorem v06_sealed_holdout_0080
    (P01 P02 P05 P10 P15 P19 P20 P21 P24 P27 P28 P30 : Point)
    (L08 L26 : Line)
    (C28 C31 : Circle)
    (h00 : circle_through_three_noncollinear_points P28 P02 P15 C31)
    (h01 : angle_bisector_line P01 P30 P15 P27 L08)
    (h02 : midpoint P21 P20 P19)
    (h03 : area_le P24 P01 P10 P19 P28 P05)
    (h04 : line_circle_intersection P19 L26 C28)
    : triangle_pred P28 P02 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0080
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0080

theorem v06_sealed_holdout_0081
    (P00 P01 P02 P05 P07 P10 P11 P12 P16 P17 P21 P22 P23 P25 P28 P29 P30 P31 : Point)
    (h00 : equilateral P17 P02 P05)
    (h01 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h02 : area_le P28 P29 P30 P31 P00 P01)
    (h03 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    (h04 : directed_angle_eq_mod_pi P02 P23 P12 P01 P22 P11)
    : triangle_pred P17 P02 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0081
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0081

theorem v06_sealed_holdout_0082
    (P00 P01 P02 P04 P06 P08 P11 P15 P18 P19 P25 P27 P29 P30 : Point)
    (L28 : Line)
    (C02 C13 C22 : Circle)
    (h00 : circle_through_three_noncollinear_points P30 P02 P15 C13)
    (h01 : area_le P00 P25 P18 P11 P04 P29)
    (h02 : angle_bisector_line P08 P01 P15 P27 L28)
    (h03 : midpoint P06 P19 P00)
    (h04 : circle_circle_intersection P19 C22 C02)
    : triangle_pred P30 P02 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0082
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0082

theorem v06_sealed_holdout_0083
    (P02 P03 P04 P05 P09 P10 P11 P13 P15 P16 P19 P20 P24 P25 P26 P27 P28 P30 : Point)
    (L12 : Line)
    (h00 : equilateral P19 P02 P05)
    (h01 : angle_bisector_line P04 P30 P15 P27 L12)
    (h02 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    (h03 : area_le P13 P28 P11 P26 P09 P24)
    (h04 : area_le P16 P09 P02 P27 P20 P13)
    : triangle_pred P19 P02 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0083
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0083

theorem v06_sealed_holdout_0084
    (P02 P03 P05 P08 P13 P17 P18 P20 P22 P23 P24 P30 P31 : Point)
    (L02 : Line)
    (C14 : Circle)
    (h00 : equilateral P20 P02 P05)
    (h01 : line_circle_intersection P03 L02 C14)
    (h02 : between P17 P24 P31)
    (h03 : between P20 P05 P22)
    (h04 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    : triangle_pred P20 P02 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0084
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0084

theorem v06_sealed_holdout_0085
    (P01 P04 P07 P10 P14 P15 P16 P17 P18 P19 P20 P21 P24 P26 P27 P30 : Point)
    (RF00 : Reflection)
    (h00 : between P26 P15 P04)
    (h01 : area_le P21 P20 P19 P18 P17 P16)
    (h02 : midpoint P24 P01 P10)
    (h03 : area_le P27 P14 P01 P20 P07 P26)
    (h04 : between P30 P27 P24)
    : reflection_image RF00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0085
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0085

theorem v06_sealed_holdout_0086
    (P00 P01 P02 P06 P12 P15 P19 P20 P23 P24 P27 P28 P29 P30 P31 : Point)
    (L10 L12 : Line)
    (C24 : Circle)
    (HOM13 : Homothety)
    (h00 : area_le P01 P24 P15 P06 P29 P20)
    (h01 : area_le P28 P29 P30 P31 P00 P01)
    (h02 : angle_bisector_line P12 P01 P15 P27 L12)
    (h03 : midpoint P02 P23 P12)
    (h04 : line_circle_intersection P19 L10 C24)
    : homothety_image HOM13 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0086
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0086

theorem v06_sealed_holdout_0087
    (P00 P01 P03 P05 P06 P08 P09 P12 P14 P15 P18 P19 P23 P26 P28 : Point)
    (C18 C19 : Circle)
    (INV30 : Inversion)
    (h00 : directed_angle_eq_mod_pi P08 P01 P26 P19 P12 P05)
    (h01 : area_le P03 P06 P09 P12 P15 P18)
    (h02 : between P06 P19 P00)
    (h03 : area_le P09 P00 P23 P14 P05 P28)
    (h04 : circle_circle_intersection P03 C18 C19)
    : inversion_image INV30 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0087
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0087

theorem v06_sealed_holdout_0088
    (P02 P09 P10 P11 P13 P15 P16 P19 P20 P22 P24 P25 P26 P27 P28 P31 : Point)
    (L10 : Line)
    (C20 : Circle)
    (SP51 : SpiralSimilarity)
    (h00 : line_circle_intersection P27 L10 C20)
    (h01 : midpoint P10 P15 P20)
    (h02 : area_le P13 P28 P11 P26 P09 P24)
    (h03 : area_le P16 P09 P02 P27 P20 P13)
    (h04 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    : spiral_similarity_center SP51 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0088
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0088

theorem v06_sealed_holdout_0089
    (P02 P04 P07 P08 P09 P13 P14 P19 P26 P27 P31 : Point)
    (C22 C30 : Circle)
    (h00 : P13 = P08)
    (h01 : P02 = P19)
    (h02 : P27 = P31)
    (h03 : circle_circle_intersection P07 C30 C22)
    (h04 : area_le P26 P31 P04 P09 P14 P19)
    : rotation_preserves_collinear P13 P02 P27 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0089
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0089

theorem v06_sealed_holdout_0090
    (P03 P07 P15 P16 P18 P19 P20 P21 P22 P24 P26 P27 P30 : Point)
    (L18 L20 : Line)
    (C02 C07 C10 C30 : Circle)
    (h00 : circle_with_center_through_point P22 P20 C07)
    (h01 : line_circle_intersection P03 L18 C10)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : area_le P30 P27 P24 P21 P18 P15)
    (h04 : angle_bisector_line P26 P07 P16 P27 L20)
    : on_circle P20 C07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0090
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0090

theorem v06_sealed_holdout_0091
    (P03 P04 P07 P11 P12 P15 P16 P22 P24 P27 P28 P29 P30 : Point)
    (L00 L04 L12 : Line)
    (C10 C18 C29 : Circle)
    (h00 : circle_through_three_noncollinear_points P11 P24 P29 C29)
    (h01 : angle_bisector_line P12 P30 P15 P27 L12)
    (h02 : circle_circle_intersection P03 C10 C18)
    (h03 : angle_bisector_line P22 P04 P15 P27 L04)
    (h04 : angle_bisector_line P27 P07 P16 P28 L00)
    : on_circle P11 C29 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0091
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0091

theorem v06_sealed_holdout_0092
    (P00 P01 P06 P07 P12 P13 P14 P15 P16 P18 P19 P26 P27 P28 : Point)
    (L12 L20 L21 : Line)
    (C05 : Circle)
    (h00 : line_circle_intersection P16 L21 C05)
    (h01 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    (h02 : angle_bisector_line P18 P01 P15 P27 L20)
    (h03 : midpoint P12 P13 P14)
    (h04 : angle_bisector_line P28 P07 P16 P27 L12)
    : on_circle P16 C05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0092
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0092

theorem v06_sealed_holdout_0093
    (P02 P03 P09 P13 P16 P19 P20 : Point)
    (L26 : Line)
    (C02 C06 C12 C18 C26 : Circle)
    (h00 : chord P13 P20 C12)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : between P16 P09 P02)
    (h03 : line_circle_intersection P19 L26 C12)
    (h04 : circle_circle_intersection P03 C26 C18)
    : on_circle P13 C12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0093
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0093

theorem v06_sealed_holdout_0094
    (P03 P04 P13 P15 P18 P19 P22 P23 P25 P27 : Point)
    (L02 L08 L18 : Line)
    (C02 C06 C14 C18 : Circle)
    (h00 : tangent_chord_angle P22 P27 P25 L02 C14)
    (h01 : line_circle_intersection P03 L18 C18)
    (h02 : between P23 P18 P13)
    (h03 : angle_bisector_line P25 P04 P15 P27 L08)
    (h04 : circle_circle_intersection P19 C06 C02)
    : on_circle P25 C14 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0094
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0094

theorem v06_sealed_holdout_0095
    (P01 P03 P04 P08 P15 P19 P22 P24 P27 P29 P30 P31 : Point)
    (L25 L26 : Line)
    (C18 C19 C20 C28 : Circle)
    (h00 : line_circle_intersection P31 L25 C20)
    (h01 : line_circle_intersection P19 L26 C28)
    (h02 : between P30 P27 P24)
    (h03 : directed_angle_eq_mod_pi P01 P08 P15 P22 P29 P04)
    (h04 : circle_circle_intersection P03 C18 C19)
    : on_line P31 L25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0095
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0095

theorem v06_sealed_holdout_0096
    (P00 P02 P03 P04 P05 P06 P08 P11 P12 P16 P17 P20 P23 P26 P27 : Point)
    (L28 L29 : Line)
    (h00 : altitude P20 P06 P11 P23 L29)
    (h01 : midpoint P02 P23 P12)
    (h02 : between P05 P04 P03)
    (h03 : between P08 P17 P26)
    (h04 : angle_bisector_line P00 P08 P16 P27 L28)
    : on_line P11 L29 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0096
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0096

theorem v06_sealed_holdout_0097
    (P03 P04 P07 P09 P10 P15 P17 P18 P27 P28 P29 P30 : Point)
    (L12 L18 L20 L24 : Line)
    (C02 : Circle)
    (h00 : angle_bisector_line P09 P10 P17 P29 L24)
    (h01 : angle_bisector_line P18 P30 P15 P27 L20)
    (h02 : line_circle_intersection P03 L18 C02)
    (h03 : angle_bisector_line P28 P04 P15 P27 L12)
    (h04 : between P18 P07 P28)
    : on_line P09 L24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0097
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0097

theorem v06_sealed_holdout_0098
    (P02 P05 P07 P09 P13 P15 P16 P19 P20 P25 P27 P29 : Point)
    (L06 L24 : Line)
    (C02 C12 C30 : Circle)
    (h00 : line_circle_intersection P02 L06 C12)
    (h01 : area_le P16 P09 P02 P27 P20 P13)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : angle_bisector_line P29 P05 P15 P27 L24)
    (h04 : midpoint P25 P16 P07)
    : on_line P02 L06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0098
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0098

theorem v06_sealed_holdout_0099
    (P00 P03 P04 P05 P08 P11 P13 P15 P18 P23 P25 P27 P29 P30 P31 : Point)
    (L04 : Line)
    (C10 C18 : Circle)
    (h00 : equilateral P15 P31 P00)
    (h01 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    (h02 : circle_circle_intersection P03 C10 C18)
    (h03 : angle_bisector_line P30 P05 P15 P27 L04)
    (h04 : area_le P00 P25 P18 P11 P04 P29)
    : equal_length P15 P31 P31 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0099
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0099

theorem v06_sealed_holdout_0100
    (P02 P03 P04 P06 P09 P15 P16 P17 P19 P20 P21 P22 P23 P28 P29 : Point)
    (L10 L26 : Line)
    (C00 C04 : Circle)
    (h00 : length_sum P20 P17 P29 P09 P16 P23)
    (h01 : area_le P03 P22 P09 P28 P15 P02)
    (h02 : line_circle_intersection P19 L10 C00)
    (h03 : midpoint P04 P21 P06)
    (h04 : line_circle_intersection P19 L26 C04)
    : length_sum P29 P09 P20 P17 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0100
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0100

theorem v06_sealed_holdout_0101
    (P03 P04 P05 P09 P10 P11 P15 P16 P17 P19 P20 P23 P27 P28 P30 P31 : Point)
    (L02 : Line)
    (C14 : Circle)
    (h00 : equal_length P17 P27 P15 P28)
    (h01 : equal_length P15 P28 P05 P16)
    (h02 : directed_angle_eq_mod_pi P10 P31 P20 P09 P30 P19)
    (h03 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h04 : line_circle_intersection P03 L02 C14)
    : equal_length P17 P27 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0101
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0101

theorem v06_sealed_holdout_0102
    (P01 P02 P03 P06 P12 P13 P19 P21 P23 P24 P31 : Point)
    (L28 : Line)
    (C02 C06 C10 C18 : Circle)
    (h00 : area_eq P06 P31 P21 P01 P12 P23)
    (h01 : area_eq P01 P12 P23 P02 P13 P24)
    (h02 : line_circle_intersection P03 L28 C02)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : circle_circle_intersection P19 C06 C02)
    : area_eq P06 P31 P21 P02 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0102
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0102

theorem v06_sealed_holdout_0103
    (P05 P07 P12 P15 P16 P19 P21 P25 P27 P28 P29 P30 : Point)
    (C14 C30 : Circle)
    (h00 : equal_length P19 P27 P15 P28)
    (h01 : equal_length P15 P28 P05 P16)
    (h02 : circle_circle_intersection P15 C14 C30)
    (h03 : area_le P25 P16 P07 P30 P21 P12)
    (h04 : midpoint P28 P29 P30)
    : equal_length P19 P27 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0103
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0103

theorem v06_sealed_holdout_0104
    (P00 P03 P04 P05 P06 P09 P14 P15 P19 P25 P26 P27 P31 : Point)
    (L00 L06 : Line)
    (C02 C06 C26 : Circle)
    (h00 : tangent_chord_angle P00 P27 P25 L06 C26)
    (h01 : area_le P26 P31 P04 P09 P14 P19)
    (h02 : circle_circle_intersection P19 C06 C02)
    (h03 : angle_bisector_line P03 P05 P15 P27 L00)
    (h04 : midpoint P03 P06 P09)
    : on_circle P25 C26 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0104
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0104

theorem v06_sealed_holdout_0105
    (P02 P03 P05 P07 P08 P09 P13 P14 P15 P16 P19 P23 P24 P27 P29 P31 : Point)
    (L08 L16 L30 : Line)
    (C02 C22 : Circle)
    (h00 : angle_bisector_line P05 P13 P23 P03 L30)
    (h01 : circle_circle_intersection P19 C22 C02)
    (h02 : angle_bisector_line P31 P02 P15 P27 L16)
    (h03 : directed_angle_eq_mod_pi P07 P02 P29 P24 P19 P14)
    (h04 : angle_bisector_line P09 P08 P16 P27 L08)
    : angle_bisector P05 P13 P23 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0105
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0105

theorem v06_sealed_holdout_0106
    (P00 P02 P03 P07 P14 P15 P16 P17 P20 P23 P24 P27 P31 : Point)
    (L02 L28 : Line)
    (C14 : Circle)
    (h00 : directed_angle_eq_mod_pi P14 P20 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : angle_bisector_line P00 P02 P15 P27 L28)
    (h03 : line_circle_intersection P03 L02 C14)
    (h04 : between P17 P24 P31)
    : directed_angle_eq_mod_pi P14 P20 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0106
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0106

theorem v06_sealed_holdout_0107
    (P01 P02 P03 P05 P06 P07 P09 P10 P15 P16 P19 P20 P21 P22 P23 P24 P25 P27 P28 P30 : Point)
    (L04 : Line)
    (h00 : directed_angle_eq_mod_2pi P03 P24 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : area_le P20 P21 P22 P23 P24 P25)
    (h03 : angle_bisector_line P06 P05 P15 P27 L04)
    (h04 : area_le P24 P01 P10 P19 P28 P05)
    : directed_angle_eq_mod_2pi P03 P24 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0107
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0107

theorem v06_sealed_holdout_0108
    (P03 P07 P08 P12 P15 P16 P17 P20 P21 P23 P24 P25 P27 P28 P29 P30 P31 : Point)
    (L12 : Line)
    (h00 : directed_angle_eq_mod_pi P16 P20 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P17 P24)
    (h02 : area_le P25 P16 P07 P30 P21 P12)
    (h03 : midpoint P28 P29 P30)
    (h04 : angle_bisector_line P12 P08 P16 P27 L12)
    : directed_angle_eq_mod_pi P16 P20 P03 P07 P17 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0108
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0108

theorem v06_sealed_holdout_0109
    (P02 P03 P05 P07 P08 P09 P15 P16 P21 P23 P24 P25 P27 P30 : Point)
    (L05 L28 : Line)
    (C18 C25 C26 : Circle)
    (h00 : directed_angle_eq_mod_2pi P05 P24 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : line_circle_intersection P23 L05 C25)
    (h03 : angle_bisector_line P08 P05 P15 P27 L28)
    (h04 : circle_circle_intersection P03 C26 C18)
    : directed_angle_eq_mod_2pi P05 P24 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0109
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0109

theorem v06_sealed_holdout_0110
    (P03 P04 P06 P11 P13 P15 P19 P21 P26 P28 : Point)
    (C02 C10 C14 C17 C18 : Circle)
    (h00 : circle_through_three_noncollinear_points P26 P03 P15 C17)
    (h01 : between P04 P21 P06)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : midpoint P13 P28 P11)
    : triangle_pred P26 P03 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0110
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0110

theorem v06_sealed_holdout_0111
    (P00 P02 P03 P05 P08 P11 P14 P15 P17 P24 P27 P31 : Point)
    (L28 : Line)
    (C18 C19 : Circle)
    (h00 : equilateral P15 P03 P05)
    (h01 : angle_bisector_line P00 P31 P15 P27 L28)
    (h02 : area_le P14 P11 P08 P05 P02 P31)
    (h03 : midpoint P17 P24 P31)
    (h04 : circle_circle_intersection P03 C18 C19)
    : triangle_pred P15 P03 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0111
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0111

theorem v06_sealed_holdout_0112
    (P01 P03 P07 P10 P14 P15 P16 P17 P18 P19 P20 P21 P24 P26 P27 P28 : Point)
    (C31 : Circle)
    (h00 : circle_through_three_noncollinear_points P28 P03 P15 C31)
    (h01 : midpoint P18 P07 P28)
    (h02 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    (h03 : between P24 P01 P10)
    (h04 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    : triangle_pred P28 P03 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0112
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0112

theorem v06_sealed_holdout_0113
    (P00 P01 P02 P03 P05 P10 P11 P12 P15 P17 P21 P22 P23 P27 P28 P29 P30 P31 : Point)
    (L20 : Line)
    (h00 : equilateral P17 P03 P05)
    (h01 : angle_bisector_line P02 P31 P15 P27 L20)
    (h02 : midpoint P28 P29 P30)
    (h03 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    (h04 : directed_angle_eq_mod_pi P02 P23 P12 P01 P22 P11)
    : triangle_pred P17 P03 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0113
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0113

theorem v06_sealed_holdout_0114
    (P00 P03 P05 P06 P09 P12 P15 P18 P19 P25 : Point)
    (L02 L10 : Line)
    (C16 C30 : Circle)
    (h00 : equilateral P18 P03 P05)
    (h01 : between P00 P25 P18)
    (h02 : area_le P03 P06 P09 P12 P15 P18)
    (h03 : line_circle_intersection P03 L02 C30)
    (h04 : line_circle_intersection P19 L10 C16)
    : triangle_pred P18 P03 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0114
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0114

theorem v06_sealed_holdout_0115
    (P01 P02 P07 P09 P10 P11 P12 P13 P14 P15 P16 P19 P20 P24 P27 P28 P29 P31 : Point)
    (RF18 : Reflection)
    (h00 : directed_angle_eq_mod_pi P12 P29 P14 P31 P16 P01)
    (h01 : directed_angle_eq_mod_pi P07 P02 P29 P24 P19 P14)
    (h02 : between P10 P15 P20)
    (h03 : between P13 P28 P11)
    (h04 : area_le P16 P09 P02 P27 P20 P13)
    : reflection_image RF18 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0115
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0115

theorem v06_sealed_holdout_0116
    (P03 P05 P11 P13 P15 P16 P18 P19 P23 P27 : Point)
    (L02 L10 L14 L16 : Line)
    (C00 C14 C16 : Circle)
    (HOM27 : Homothety)
    (h00 : line_circle_intersection P11 L14 C16)
    (h01 : line_circle_intersection P03 L02 C14)
    (h02 : line_circle_intersection P19 L10 C00)
    (h03 : angle_bisector_line P15 P05 P16 P27 L16)
    (h04 : between P23 P18 P13)
    : homothety_image HOM27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0116
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0116

theorem v06_sealed_holdout_0117
    (P01 P08 P10 P14 P16 P19 P21 P23 P24 P27 : Point)
    (L10 L24 : Line)
    (C06 C24 C30 : Circle)
    (INV40 : Inversion)
    (h00 : circle_circle_intersection P23 C30 C06)
    (h01 : line_circle_intersection P19 L10 C24)
    (h02 : between P24 P01 P10)
    (h03 : midpoint P27 P14 P01)
    (h04 : angle_bisector_line P21 P08 P16 P27 L24)
    : inversion_image INV40 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0117
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0117

theorem v06_sealed_holdout_0118
    (P00 P01 P02 P03 P04 P05 P09 P13 P15 P17 P19 P27 P28 P29 P30 P31 : Point)
    (L04 L08 : Line)
    (C02 C14 : Circle)
    (SP57 : SpiralSimilarity)
    (h00 : angle_bisector_line P02 P09 P31 P13 L04)
    (h01 : area_le P28 P29 P30 P31 P00 P01)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : angle_bisector_line P17 P05 P15 P27 L08)
    (h04 : area_le P05 P04 P03 P02 P01 P00)
    : spiral_similarity_center SP57 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0118
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0118

theorem v06_sealed_holdout_0119
    (P01 P03 P08 P11 P19 P26 P27 P31 : Point)
    (C18 C19 : Circle)
    (h00 : P11 = P08)
    (h01 : P03 = P19)
    (h02 : P27 = P31)
    (h03 : midpoint P08 P01 P26)
    (h04 : circle_circle_intersection P03 C18 C19)
    : rotation_preserves_collinear P11 P03 P27 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0119
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0119

theorem v06_sealed_holdout_0120
    (P02 P09 P10 P15 P16 P19 P20 P21 P22 P25 P28 P31 : Point)
    (C02 C06 C11 : Circle)
    (h00 : circle_with_center_through_point P20 P21 C11)
    (h01 : midpoint P10 P15 P20)
    (h02 : circle_circle_intersection P19 C06 C02)
    (h03 : midpoint P16 P09 P02)
    (h04 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    : on_circle P21 C11 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0120
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0120

theorem v06_sealed_holdout_0121
    (P02 P04 P05 P09 P14 P15 P16 P19 P20 P25 P26 P27 P29 P31 : Point)
    (L10 L12 L16 : Line)
    (C00 C31 : Circle)
    (h00 : circle_through_three_noncollinear_points P09 P25 P29 C31)
    (h01 : line_circle_intersection P19 L10 C00)
    (h02 : angle_bisector_line P15 P02 P16 P27 L16)
    (h03 : angle_bisector_line P20 P05 P15 P27 L12)
    (h04 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    : on_circle P09 C31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0121
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0121

theorem v06_sealed_holdout_0122
    (P01 P02 P05 P10 P14 P15 P16 P18 P19 P21 P24 P27 P28 P30 : Point)
    (L10 L21 L28 : Line)
    (C00 C19 : Circle)
    (h00 : line_circle_intersection P14 L21 C19)
    (h01 : area_le P24 P01 P10 P19 P28 P05)
    (h02 : angle_bisector_line P16 P02 P15 P27 L28)
    (h03 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    (h04 : line_circle_intersection P19 L10 C00)
    : on_circle P14 C19 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0122
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0122

theorem v06_sealed_holdout_0123
    (P00 P03 P04 P05 P08 P10 P11 P17 P21 P22 P26 P31 : Point)
    (C10 C18 C20 : Circle)
    (h00 : chord P11 P21 C20)
    (h01 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    (h02 : circle_circle_intersection P03 C10 C18)
    (h03 : between P05 P04 P03)
    (h04 : midpoint P08 P17 P26)
    : on_circle P11 C20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0123
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0123

theorem v06_sealed_holdout_0124
    (P00 P01 P05 P06 P07 P09 P12 P13 P14 P15 P16 P17 P18 P23 P26 P27 P28 : Point)
    (L29 : Line)
    (C04 : Circle)
    (h00 : line_circle_intersection P01 L29 C04)
    (h01 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h02 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h03 : between P15 P26 P05)
    (h04 : area_le P18 P07 P28 P17 P06 P27)
    : on_line P01 L29 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0124
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0124

theorem v06_sealed_holdout_0125
    (P02 P03 P09 P13 P16 P19 P20 P22 P27 P29 : Point)
    (L27 : Line)
    (C02 C04 C06 C30 : Circle)
    (h00 : line_circle_intersection P29 L27 C04)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : area_le P16 P09 P02 P27 P20 P13)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : midpoint P22 P03 P16)
    : on_line P29 L27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0125
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0125

theorem v06_sealed_holdout_0126
    (P03 P05 P07 P09 P11 P13 P18 P19 P20 P22 P23 P24 : Point)
    (L02 L03 L10 : Line)
    (C08 C22 : Circle)
    (h00 : altitude P18 P07 P11 P23 L03)
    (h01 : directed_angle_eq_mod_pi P20 P05 P22 P07 P24 P09)
    (h02 : between P23 P18 P13)
    (h03 : line_circle_intersection P03 L02 C22)
    (h04 : line_circle_intersection P19 L10 C08)
    : on_line P11 L03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0126
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0126

theorem v06_sealed_holdout_0127
    (P01 P02 P04 P06 P07 P08 P10 P14 P15 P17 P21 P27 P29 : Point)
    (L24 L28 : Line)
    (h00 : angle_bisector_line P07 P10 P17 P29 L28)
    (h01 : between P27 P14 P01)
    (h02 : angle_bisector_line P21 P02 P15 P27 L24)
    (h03 : between P01 P08 P15)
    (h04 : midpoint P04 P21 P06)
    : on_line P07 L28 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0127
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0127

theorem v06_sealed_holdout_0128
    (P00 P01 P02 P03 P04 P10 P11 P12 P17 P19 P22 P23 P30 : Point)
    (L08 L18 : Line)
    (C02 C06 C10 C28 : Circle)
    (h00 : line_circle_intersection P00 L08 C28)
    (h01 : directed_angle_eq_mod_pi P02 P23 P12 P01 P22 P11)
    (h02 : circle_circle_intersection P19 C06 C02)
    (h03 : line_circle_intersection P03 L18 C10)
    (h04 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    : on_line P00 L08 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0128
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0128

theorem v06_sealed_holdout_0129
    (P00 P03 P05 P13 P15 P19 P26 P31 : Point)
    (L02 : Line)
    (C02 C06 C18 C19 C22 : Circle)
    (h00 : equilateral P13 P00 P31)
    (h01 : circle_circle_intersection P19 C22 C02)
    (h02 : circle_circle_intersection P03 C18 C19)
    (h03 : between P15 P26 P05)
    (h04 : line_circle_intersection P03 L02 C06)
    : equal_length P13 P00 P00 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0129
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0129

theorem v06_sealed_holdout_0130
    (P03 P07 P09 P16 P17 P18 P19 P22 P23 P25 P29 : Point)
    (L00 : Line)
    (C02 C30 : Circle)
    (h00 : length_sum P18 P17 P29 P09 P16 P23)
    (h01 : line_circle_intersection P19 L00 C30)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : midpoint P22 P03 P16)
    (h04 : midpoint P25 P16 P07)
    : length_sum P29 P09 P18 P17 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0130
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0130

theorem v06_sealed_holdout_0131
    (P00 P05 P15 P16 P17 P18 P19 P25 P27 P28 P31 : Point)
    (C02 C06 C14 C15 : Circle)
    (h00 : equal_length P15 P28 P16 P27)
    (h01 : equal_length P16 P27 P05 P17)
    (h02 : circle_circle_intersection P31 C14 C15)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : midpoint P00 P25 P18)
    : equal_length P15 P28 P05 P17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0131
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0131

theorem v06_sealed_holdout_0132
    (P00 P01 P02 P04 P06 P09 P12 P13 P16 P19 P21 P23 P24 P31 : Point)
    (L20 L26 : Line)
    (C04 : Circle)
    (h00 : area_eq P04 P00 P21 P01 P12 P23)
    (h01 : area_eq P01 P12 P23 P02 P13 P24)
    (h02 : angle_bisector_line P16 P09 P31 P13 L20)
    (h03 : between P04 P21 P06)
    (h04 : line_circle_intersection P19 L26 C04)
    : area_eq P04 P00 P21 P02 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0132
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0132

theorem v06_sealed_holdout_0133
    (P04 P05 P08 P10 P11 P14 P15 P16 P17 P20 P23 P27 P28 P30 P31 : Point)
    (h00 : equal_length P17 P28 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : midpoint P10 P31 P20)
    (h03 : area_le P11 P30 P17 P04 P23 P10)
    (h04 : midpoint P14 P11 P08)
    : equal_length P17 P28 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0133
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0133

theorem v06_sealed_holdout_0134
    (P03 P05 P06 P07 P09 P15 P16 P17 P18 P25 P26 P27 P28 P30 : Point)
    (L04 L18 : Line)
    (C18 C19 C30 : Circle)
    (h00 : tangent_chord_angle P30 P28 P25 L18 C30)
    (h01 : circle_circle_intersection P03 C18 C19)
    (h02 : area_le P15 P26 P05 P16 P27 P06)
    (h03 : directed_angle_eq_mod_pi P18 P07 P28 P17 P06 P27)
    (h04 : angle_bisector_line P06 P09 P16 P27 L04)
    : on_circle P25 C30 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0134
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0134

theorem v06_sealed_holdout_0135
    (P03 P04 P07 P12 P14 P16 P19 P21 P22 P23 P25 P28 P29 P30 : Point)
    (L00 L26 : Line)
    (C12 : Circle)
    (h00 : angle_bisector_line P03 P14 P23 P04 L00)
    (h01 : line_circle_intersection P19 L26 C12)
    (h02 : between P22 P03 P16)
    (h03 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h04 : midpoint P28 P29 P30)
    : angle_bisector P03 P14 P23 P04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0135
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0135

theorem v06_sealed_holdout_0136
    (P03 P06 P07 P12 P15 P16 P19 P21 P23 P24 P27 P30 P31 : Point)
    (L00 L04 : Line)
    (C02 C30 : Circle)
    (h00 : directed_angle_eq_mod_pi P12 P21 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : angle_bisector_line P30 P03 P15 P27 L04)
    (h03 : angle_bisector_line P03 P06 P15 P27 L00)
    (h04 : circle_circle_intersection P19 C30 C02)
    : directed_angle_eq_mod_pi P12 P21 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0136
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0136

theorem v06_sealed_holdout_0137
    (P01 P02 P03 P07 P09 P16 P21 P25 P26 P29 P30 : Point)
    (L02 L09 : Line)
    (C21 C22 : Circle)
    (h00 : directed_angle_eq_mod_2pi P01 P25 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P26 P02)
    (h02 : line_circle_intersection P07 L09 C21)
    (h03 : midpoint P07 P02 P29)
    (h04 : line_circle_intersection P03 L02 C22)
    : directed_angle_eq_mod_2pi P01 P25 P09 P16 P26 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0137
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0137

theorem v06_sealed_holdout_0138
    (P02 P03 P04 P05 P07 P08 P09 P10 P11 P14 P15 P16 P17 P21 P23 P24 P27 P30 P31 : Point)
    (L20 : Line)
    (h00 : directed_angle_eq_mod_pi P14 P21 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h03 : area_le P14 P11 P08 P05 P02 P31)
    (h04 : angle_bisector_line P10 P09 P16 P27 L20)
    : directed_angle_eq_mod_pi P14 P21 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0138
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0138

theorem v06_sealed_holdout_0139
    (P02 P03 P07 P09 P10 P13 P16 P17 P18 P19 P20 P21 P23 P25 P26 P30 P31 : Point)
    (L12 L18 : Line)
    (C10 : Circle)
    (h00 : directed_angle_eq_mod_2pi P03 P25 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P26 P02)
    (h02 : angle_bisector_line P23 P10 P31 P13 L12)
    (h03 : area_le P21 P20 P19 P18 P17 P16)
    (h04 : line_circle_intersection P03 L18 C10)
    : directed_angle_eq_mod_2pi P03 P25 P09 P16 P26 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0139
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0139

theorem v06_sealed_holdout_0140
    (P03 P04 P06 P07 P09 P10 P12 P15 P16 P22 P23 P24 P25 P27 P29 : Point)
    (L12 L16 : Line)
    (C03 : Circle)
    (h00 : circle_through_three_noncollinear_points P24 P04 P15 C03)
    (h01 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    (h02 : midpoint P25 P16 P07)
    (h03 : angle_bisector_line P07 P06 P15 P27 L16)
    (h04 : angle_bisector_line P12 P09 P16 P27 L12)
    : triangle_pred P24 P04 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0140
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0140

theorem v06_sealed_holdout_0141
    (P00 P03 P04 P05 P06 P08 P09 P10 P12 P13 P15 P18 P19 P25 P27 P29 : Point)
    (h00 : equilateral P13 P04 P05)
    (h01 : directed_angle_eq_mod_pi P29 P12 P27 P10 P25 P08)
    (h02 : between P00 P25 P18)
    (h03 : area_le P03 P06 P09 P12 P15 P18)
    (h04 : midpoint P06 P19 P00)
    : triangle_pred P13 P04 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0141
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0141

theorem v06_sealed_holdout_0142
    (P03 P04 P10 P15 P19 P20 P26 : Point)
    (L10 L18 : Line)
    (C02 C08 C14 C17 C18 : Circle)
    (h00 : circle_through_three_noncollinear_points P26 P04 P15 C17)
    (h01 : line_circle_intersection P03 L18 C18)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : midpoint P10 P15 P20)
    (h04 : line_circle_intersection P19 L10 C08)
    : triangle_pred P26 P04 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0142
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0142

theorem v06_sealed_holdout_0143
    (P04 P05 P07 P08 P09 P11 P14 P15 P17 P20 P22 P24 P30 P31 : Point)
    (h00 : equilateral P15 P04 P05)
    (h01 : between P11 P30 P17)
    (h02 : between P14 P11 P08)
    (h03 : midpoint P17 P24 P31)
    (h04 : directed_angle_eq_mod_pi P20 P05 P22 P07 P24 P09)
    : triangle_pred P15 P04 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0143
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0143

theorem v06_sealed_holdout_0144
    (P01 P03 P04 P05 P10 P16 P17 P18 P19 P20 P21 P24 : Point)
    (L02 L26 : Line)
    (C06 C28 : Circle)
    (h00 : equilateral P16 P04 P05)
    (h01 : line_circle_intersection P03 L02 C06)
    (h02 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    (h03 : between P24 P01 P10)
    (h04 : line_circle_intersection P19 L26 C28)
    : triangle_pred P16 P04 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0144
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0144

theorem v06_sealed_holdout_0145
    (P00 P02 P03 P07 P10 P11 P12 P16 P21 P22 P23 P25 P31 : Point)
    (L18 : Line)
    (C02 C22 C30 : Circle)
    (RF36 : Reflection)
    (h00 : circle_circle_intersection P07 C30 C22)
    (h01 : between P25 P16 P07)
    (h02 : line_circle_intersection P03 L18 C02)
    (h03 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    (h04 : between P02 P23 P12)
    : reflection_image RF36 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0145
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0145

theorem v06_sealed_holdout_0146
    (P03 P06 P09 P10 P13 P19 P30 P31 : Point)
    (L04 L18 : Line)
    (C02 C18 C22 C26 : Circle)
    (HOM41 : Homothety)
    (h00 : angle_bisector_line P30 P10 P31 P13 L04)
    (h01 : line_circle_intersection P03 L18 C26)
    (h02 : between P03 P06 P09)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : circle_circle_intersection P19 C22 C02)
    : homothety_image HOM41 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0146
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0146

theorem v06_sealed_holdout_0147
    (P02 P03 P09 P10 P11 P12 P13 P14 P15 P16 P19 P20 P24 P25 P26 P27 P28 P29 P30 : Point)
    (L26 : Line)
    (C04 : Circle)
    (INV50 : Inversion)
    (h00 : midpoint P12 P29 P14)
    (h01 : line_circle_intersection P19 L26 C04)
    (h02 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    (h03 : area_le P13 P28 P11 P26 P09 P24)
    (h04 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    : inversion_image INV50 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0147
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0147

theorem v06_sealed_holdout_0148
    (P03 P05 P06 P13 P17 P18 P19 P20 P22 P23 P24 P25 P31 : Point)
    (C18 C26 : Circle)
    (SP63 : SpiralSimilarity)
    (h00 : between P19 P06 P25)
    (h01 : circle_circle_intersection P03 C26 C18)
    (h02 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    (h03 : between P20 P05 P22)
    (h04 : between P23 P18 P13)
    : spiral_similarity_center SP63 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0148
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0148

theorem v06_sealed_holdout_0149
    (P03 P04 P08 P09 P14 P15 P18 P19 P21 P24 P25 P26 P27 P30 P31 : Point)
    (h00 : P09 = P08)
    (h01 : P04 = P19)
    (h02 : P27 = P31)
    (h03 : area_le P26 P15 P04 P25 P14 P03)
    (h04 : area_le P30 P27 P24 P21 P18 P15)
    : rotation_preserves_collinear P09 P04 P27 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0149
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0149

theorem v06_sealed_holdout_0150
    (P03 P04 P05 P06 P15 P17 P18 P19 P22 P27 P28 P29 P30 : Point)
    (L08 : Line)
    (C02 C14 C15 : Circle)
    (h00 : circle_with_center_through_point P18 P22 C15)
    (h01 : between P28 P29 P30)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : angle_bisector_line P17 P06 P15 P27 L08)
    (h04 : between P05 P04 P03)
    : on_circle P22 C15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0150
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0150

theorem v06_sealed_holdout_0151
    (P00 P03 P05 P07 P09 P12 P13 P14 P15 P16 P17 P19 P23 P26 P28 P29 : Point)
    (L26 : Line)
    (C01 C12 C18 C26 : Circle)
    (h00 : circle_through_three_noncollinear_points P07 P26 P29 C01)
    (h01 : line_circle_intersection P19 L26 C12)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h04 : area_le P12 P13 P14 P15 P16 P17)
    : on_circle P07 C01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0151
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0151

theorem v06_sealed_holdout_0152
    (P02 P03 P09 P10 P11 P12 P13 P15 P19 P20 P22 P24 P25 P26 P28 P31 : Point)
    (L18 L21 : Line)
    (C01 C26 : Circle)
    (h00 : line_circle_intersection P12 L21 C01)
    (h01 : midpoint P10 P15 P20)
    (h02 : directed_angle_eq_mod_pi P13 P28 P11 P26 P09 P24)
    (h03 : line_circle_intersection P03 L18 C26)
    (h04 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    : on_circle P12 C01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0152
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0152

theorem v06_sealed_holdout_0153
    (P04 P05 P09 P13 P14 P18 P19 P20 P22 P23 P26 P31 : Point)
    (L10 : Line)
    (C00 C28 : Circle)
    (h00 : chord P09 P22 C28)
    (h01 : line_circle_intersection P19 L10 C00)
    (h02 : midpoint P20 P05 P22)
    (h03 : between P23 P18 P13)
    (h04 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    : on_circle P09 C28 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0153
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0153

theorem v06_sealed_holdout_0154
    (P01 P03 P05 P07 P14 P16 P20 P24 P26 P27 P30 P31 : Point)
    (L18 L20 L31 : Line)
    (C18 C20 : Circle)
    (h00 : line_circle_intersection P31 L31 C20)
    (h01 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    (h02 : between P30 P27 P24)
    (h03 : angle_bisector_line P26 P05 P16 P27 L20)
    (h04 : line_circle_intersection P03 L18 C18)
    : on_line P31 L31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0154
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0154

theorem v06_sealed_holdout_0155
    (P00 P01 P02 P06 P09 P10 P11 P12 P15 P16 P21 P22 P23 P27 P28 P31 : Point)
    (L00 L04 L29 : Line)
    (C20 : Circle)
    (h00 : line_circle_intersection P27 L29 C20)
    (h01 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    (h02 : area_le P02 P23 P12 P01 P22 P11)
    (h03 : angle_bisector_line P22 P06 P15 P27 L04)
    (h04 : angle_bisector_line P27 P09 P16 P28 L00)
    : on_line P27 L29 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0155
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0155

theorem v06_sealed_holdout_0156
    (P00 P03 P05 P06 P07 P08 P09 P11 P13 P14 P15 P16 P19 P23 P26 P27 P28 : Point)
    (L09 L18 : Line)
    (C02 : Circle)
    (h00 : altitude P16 P08 P11 P23 L09)
    (h01 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    (h02 : area_le P09 P00 P23 P14 P05 P28)
    (h03 : line_circle_intersection P03 L18 C02)
    (h04 : area_le P15 P26 P05 P16 P27 P06)
    : on_line P11 L09 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0156
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0156

theorem v06_sealed_holdout_0157
    (P00 P02 P03 P05 P10 P11 P14 P15 P16 P17 P19 P22 P23 P25 P27 P28 P29 P31 : Point)
    (L00 L04 L18 : Line)
    (C26 : Circle)
    (h00 : angle_bisector_line P05 P11 P17 P29 L00)
    (h01 : angle_bisector_line P14 P00 P15 P27 L04)
    (h02 : line_circle_intersection P03 L18 C26)
    (h03 : area_le P19 P22 P25 P28 P31 P02)
    (h04 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    : on_line P05 L00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0157
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0157

theorem v06_sealed_holdout_0158
    (P03 P04 P08 P10 P12 P13 P18 P23 P25 P26 P27 P29 P30 P31 : Point)
    (L10 L18 : Line)
    (C12 C18 : Circle)
    (h00 : line_circle_intersection P30 L10 C12)
    (h01 : line_circle_intersection P03 L18 C18)
    (h02 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    (h03 : between P26 P31 P04)
    (h04 : directed_angle_eq_mod_pi P29 P12 P27 P10 P25 P08)
    : on_line P30 L10 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0158
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0158

theorem v06_sealed_holdout_0159
    (P01 P04 P06 P11 P14 P15 P21 P24 P26 P27 P30 P31 : Point)
    (L20 : Line)
    (h00 : equilateral P11 P01 P31)
    (h01 : midpoint P27 P14 P01)
    (h02 : between P30 P27 P24)
    (h03 : angle_bisector_line P26 P06 P15 P27 L20)
    (h04 : between P04 P21 P06)
    : equal_length P11 P01 P01 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0159
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0159

theorem v06_sealed_holdout_0160
    (P03 P04 P05 P08 P09 P10 P11 P12 P13 P16 P17 P18 P23 P26 P29 P30 P31 : Point)
    (L20 : Line)
    (h00 : length_sum P16 P18 P29 P09 P17 P23)
    (h01 : angle_bisector_line P12 P10 P31 P13 L20)
    (h02 : midpoint P05 P04 P03)
    (h03 : midpoint P08 P17 P26)
    (h04 : midpoint P11 P30 P17)
    : length_sum P29 P09 P16 P18 P17 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0160
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0160

theorem v06_sealed_holdout_0161
    (P05 P06 P07 P08 P13 P14 P15 P16 P17 P18 P19 P27 P28 P29 : Point)
    (L26 : Line)
    (C20 : Circle)
    (h00 : equal_length P13 P29 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : midpoint P14 P27 P08)
    (h03 : line_circle_intersection P19 L26 C20)
    (h04 : directed_angle_eq_mod_pi P18 P07 P28 P17 P06 P27)
    : equal_length P13 P29 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0161
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0161

theorem v06_sealed_holdout_0162
    (P01 P02 P03 P04 P07 P12 P13 P16 P19 P21 P23 P24 P25 P30 : Point)
    (C18 C26 : Circle)
    (h00 : area_eq P02 P01 P21 P03 P12 P23)
    (h01 : area_eq P03 P12 P23 P04 P13 P24)
    (h02 : between P21 P04 P19)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    : area_eq P02 P01 P21 P04 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0162
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0162

theorem v06_sealed_holdout_0163
    (P00 P04 P05 P11 P12 P13 P15 P16 P17 P18 P25 P27 P28 P29 P30 : Point)
    (h00 : equal_length P15 P29 P16 P27)
    (h01 : equal_length P16 P27 P05 P17)
    (h02 : area_le P28 P13 P30 P15 P00 P17)
    (h03 : midpoint P29 P12 P27)
    (h04 : area_le P00 P25 P18 P11 P04 P29)
    : equal_length P15 P29 P05 P17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0163
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0163

theorem v06_sealed_holdout_0164
    (P02 P03 P05 P07 P10 P14 P15 P16 P19 P20 P24 P25 P26 P27 P29 P30 P31 : Point)
    (L04 L18 L20 : Line)
    (C18 : Circle)
    (h00 : angle_bisector_line P05 P14 P24 P03 L04)
    (h01 : angle_bisector_line P26 P31 P16 P27 L20)
    (h02 : line_circle_intersection P03 L18 C18)
    (h03 : directed_angle_eq_mod_pi P07 P02 P29 P24 P19 P14)
    (h04 : area_le P10 P15 P20 P25 P30 P03)
    : angle_bisector P05 P14 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0164
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0164

theorem v06_sealed_holdout_0165
    (P01 P03 P04 P05 P08 P11 P12 P14 P15 P17 P19 P21 P23 P26 : Point)
    (L02 : Line)
    (C02 C30 : Circle)
    (h00 : angle_bisector_line P01 P15 P23 P03 L02)
    (h01 : between P05 P04 P03)
    (h02 : area_le P08 P17 P26 P03 P12 P21)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : midpoint P14 P11 P08)
    : angle_bisector P01 P15 P23 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0165
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0165

theorem v06_sealed_holdout_0166
    (P03 P05 P07 P10 P15 P16 P19 P22 P23 P24 P26 P31 : Point)
    (L02 : Line)
    (C02 C06 : Circle)
    (h00 : directed_angle_eq_mod_pi P10 P22 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : between P15 P26 P05)
    (h03 : line_circle_intersection P03 L02 C06)
    (h04 : circle_circle_intersection P19 C06 C02)
    : directed_angle_eq_mod_pi P10 P22 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0166
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0166

theorem v06_sealed_holdout_0167
    (P02 P07 P09 P10 P12 P13 P16 P19 P21 P25 P26 P27 P30 P31 : Point)
    (L12 L16 : Line)
    (h00 : directed_angle_eq_mod_2pi P31 P26 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : angle_bisector_line P19 P10 P31 P13 L12)
    (h03 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h04 : angle_bisector_line P07 P10 P16 P27 L16)
    : directed_angle_eq_mod_2pi P31 P26 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0167
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0167

theorem v06_sealed_holdout_0168
    (P03 P06 P07 P08 P09 P10 P12 P15 P16 P18 P22 P23 P24 P25 P27 P29 P31 : Point)
    (L00 : Line)
    (h00 : directed_angle_eq_mod_pi P12 P22 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : directed_angle_eq_mod_pi P29 P12 P27 P10 P25 P08)
    (h03 : angle_bisector_line P03 P07 P16 P27 L00)
    (h04 : directed_angle_eq_mod_pi P03 P06 P09 P12 P15 P18)
    : directed_angle_eq_mod_pi P12 P22 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0168
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0168

theorem v06_sealed_holdout_0169
    (P00 P01 P02 P03 P04 P06 P07 P09 P16 P21 P25 P26 P27 P30 : Point)
    (L12 : Line)
    (C10 C18 : Circle)
    (h00 : directed_angle_eq_mod_2pi P01 P26 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : between P06 P03 P00)
    (h03 : angle_bisector_line P04 P07 P16 P27 L12)
    (h04 : circle_circle_intersection P03 C10 C18)
    : directed_angle_eq_mod_2pi P01 P26 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0169
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0169

theorem v06_sealed_holdout_0170
    (P03 P05 P08 P11 P14 P15 P17 P19 P22 P30 : Point)
    (C02 C18 C21 C22 : Circle)
    (h00 : circle_through_three_noncollinear_points P22 P05 P15 C21)
    (h01 : circle_circle_intersection P03 C02 C18)
    (h02 : midpoint P11 P30 P17)
    (h03 : between P14 P11 P08)
    (h04 : circle_circle_intersection P19 C22 C02)
    : triangle_pred P22 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0170
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0170

theorem v06_sealed_holdout_0171
    (P01 P05 P06 P07 P10 P11 P15 P18 P19 P20 P21 P24 P26 P28 : Point)
    (h00 : equilateral P11 P05 P06)
    (h01 : between P15 P26 P05)
    (h02 : midpoint P18 P07 P28)
    (h03 : between P21 P20 P19)
    (h04 : area_le P24 P01 P10 P19 P28 P05)
    : triangle_pred P11 P05 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0171
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0171

theorem v06_sealed_holdout_0172
    (P00 P02 P03 P04 P05 P10 P11 P15 P16 P21 P22 P24 P27 P28 P29 P30 P31 : Point)
    (L20 : Line)
    (C03 : Circle)
    (h00 : circle_through_three_noncollinear_points P24 P05 P15 C03)
    (h01 : between P22 P03 P16)
    (h02 : angle_bisector_line P02 P04 P15 P27 L20)
    (h03 : midpoint P28 P29 P30)
    (h04 : area_le P31 P10 P21 P00 P11 P22)
    : triangle_pred P24 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0172
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0172

theorem v06_sealed_holdout_0173
    (P00 P05 P06 P07 P13 P18 P19 P25 P26 : Point)
    (C02 C06 C30 : Circle)
    (h00 : equilateral P13 P05 P06)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : midpoint P00 P25 P18)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : area_le P06 P19 P00 P13 P26 P07)
    : triangle_pred P13 P05 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0173
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0173

theorem v06_sealed_holdout_0174
    (P02 P03 P04 P05 P06 P07 P08 P14 P19 P21 P23 P24 P25 P29 : Point)
    (L10 : Line)
    (C08 C10 C18 : Circle)
    (h00 : equilateral P14 P05 P06)
    (h01 : area_le P04 P21 P06 P23 P08 P25)
    (h02 : area_le P07 P02 P29 P24 P19 P14)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : line_circle_intersection P19 L10 C08)
    : triangle_pred P14 P05 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0174
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0174

theorem v06_sealed_holdout_0175
    (P02 P04 P05 P08 P10 P11 P14 P16 P17 P19 P20 P22 P23 P25 P30 : Point)
    (C02 C22 : Circle)
    (RF54 : Reflection)
    (h00 : midpoint P16 P25 P02)
    (h01 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h02 : midpoint P14 P11 P08)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : between P20 P05 P22)
    : reflection_image RF54 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0175
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0175

theorem v06_sealed_holdout_0176
    (P01 P02 P03 P07 P13 P14 P19 P20 P23 P26 P27 : Point)
    (L10 : Line)
    (C02 C10 C18 C24 : Circle)
    (HOM55 : Homothety)
    (h00 : between P23 P02 P13)
    (h01 : circle_circle_intersection P03 C10 C18)
    (h02 : line_circle_intersection P19 L10 C24)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    : homothety_image HOM55 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0176
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0176

theorem v06_sealed_holdout_0177
    (P01 P02 P05 P07 P11 P12 P15 P16 P18 P22 P23 P24 P27 P28 P29 P30 P31 : Point)
    (L12 L20 : Line)
    (INV60 : Inversion)
    (h00 : area_le P30 P11 P24 P05 P18 P31)
    (h01 : angle_bisector_line P02 P01 P15 P27 L20)
    (h02 : midpoint P28 P29 P30)
    (h03 : angle_bisector_line P12 P07 P16 P27 L12)
    (h04 : area_le P02 P23 P12 P01 P22 P11)
    : inversion_image INV60 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0177
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0177

theorem v06_sealed_holdout_0178
    (P01 P03 P05 P06 P09 P15 P16 P18 P19 P20 P27 : Point)
    (L00 L02 : Line)
    (C02 C22 C30 : Circle)
    (SP05 : SpiralSimilarity)
    (h00 : directed_angle_eq_mod_pi P05 P20 P03 P18 P01 P16)
    (h01 : angle_bisector_line P03 P01 P15 P27 L00)
    (h02 : midpoint P03 P06 P09)
    (h03 : line_circle_intersection P03 L02 C30)
    (h04 : circle_circle_intersection P19 C22 C02)
    : spiral_similarity_center SP05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0178
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0178

theorem v06_sealed_holdout_0179
    (P05 P07 P08 P10 P16 P19 P27 P31 : Point)
    (L00 L31 : Line)
    (C31 : Circle)
    (h00 : P07 = P08)
    (h01 : P05 = P19)
    (h02 : P27 = P31)
    (h03 : line_circle_intersection P31 L31 C31)
    (h04 : angle_bisector_line P19 P10 P16 P27 L00)
    : rotation_preserves_collinear P07 P05 P27 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0179
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0179

theorem v06_sealed_holdout_0180
    (P02 P05 P08 P11 P13 P14 P16 P18 P19 P20 P22 P23 P31 : Point)
    (L10 : Line)
    (C00 C19 : Circle)
    (h00 : circle_with_center_through_point P16 P23 C19)
    (h01 : area_le P14 P11 P08 P05 P02 P31)
    (h02 : line_circle_intersection P19 L10 C00)
    (h03 : midpoint P20 P05 P22)
    (h04 : midpoint P23 P18 P13)
    : on_circle P23 C19 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0180
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0180

theorem v06_sealed_holdout_0181
    (P01 P05 P07 P10 P14 P15 P18 P19 P20 P21 P24 P26 P27 P28 P30 : Point)
    (C03 : Circle)
    (h00 : circle_through_three_noncollinear_points P05 P27 P30 C03)
    (h01 : between P21 P20 P19)
    (h02 : area_le P24 P01 P10 P19 P28 P05)
    (h03 : area_le P27 P14 P01 P20 P07 P26)
    (h04 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    : on_circle P05 C03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0181
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0181

theorem v06_sealed_holdout_0182
    (P00 P01 P02 P10 P11 P12 P19 P21 P22 P23 P28 P29 P30 P31 : Point)
    (L10 L21 : Line)
    (C15 C24 : Circle)
    (h00 : line_circle_intersection P10 L21 C15)
    (h01 : between P28 P29 P30)
    (h02 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    (h03 : directed_angle_eq_mod_pi P02 P23 P12 P01 P22 P11)
    (h04 : line_circle_intersection P19 L10 C24)
    : on_circle P10 C15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0182
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0182

theorem v06_sealed_holdout_0183
    (P00 P03 P06 P07 P09 P12 P13 P14 P15 P18 P23 : Point)
    (C04 C18 C26 : Circle)
    (h00 : chord P07 P23 C04)
    (h01 : directed_angle_eq_mod_pi P03 P06 P09 P12 P15 P18)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : between P09 P00 P23)
    (h04 : midpoint P12 P13 P14)
    : on_circle P07 C04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0183
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0183

theorem v06_sealed_holdout_0184
    (P03 P06 P11 P13 P16 P19 P22 P24 P27 P28 P29 : Point)
    (L00 L01 L28 : Line)
    (C04 : Circle)
    (h00 : line_circle_intersection P29 L01 C04)
    (h01 : midpoint P13 P28 P11)
    (h02 : angle_bisector_line P19 P03 P16 P27 L00)
    (h03 : angle_bisector_line P24 P06 P16 P27 L28)
    (h04 : between P22 P03 P16)
    : on_line P29 L01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0184
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0184

theorem v06_sealed_holdout_0185
    (P04 P05 P06 P07 P09 P13 P17 P19 P20 P22 P24 P25 P26 P31 : Point)
    (L26 L31 : Line)
    (C04 : Circle)
    (h00 : line_circle_intersection P25 L31 C04)
    (h01 : area_le P17 P24 P31 P06 P13 P20)
    (h02 : area_le P20 P05 P22 P07 P24 P09)
    (h03 : line_circle_intersection P19 L26 C04)
    (h04 : between P26 P31 P04)
    : on_line P25 L31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0185
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0185

theorem v06_sealed_holdout_0186
    (P01 P03 P04 P08 P09 P11 P14 P15 P16 P18 P21 P23 P24 P27 P30 : Point)
    (L15 L18 L28 : Line)
    (C10 : Circle)
    (h00 : altitude P14 P09 P11 P23 L15)
    (h01 : line_circle_intersection P03 L18 C10)
    (h02 : angle_bisector_line P16 P04 P15 P27 L28)
    (h03 : area_le P30 P27 P24 P21 P18 P15)
    (h04 : between P01 P08 P15)
    : on_line P11 L15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0186
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0186

theorem v06_sealed_holdout_0187
    (P00 P01 P02 P03 P08 P10 P11 P12 P17 P19 P21 P22 P23 P26 P29 P31 : Point)
    (L04 : Line)
    (C02 C06 : Circle)
    (h00 : angle_bisector_line P03 P12 P17 P29 L04)
    (h01 : area_le P31 P10 P21 P00 P11 P22)
    (h02 : area_le P02 P23 P12 P01 P22 P11)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : midpoint P08 P17 P26)
    : on_line P03 L04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0187
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0187

theorem v06_sealed_holdout_0188
    (P00 P06 P10 P12 P13 P14 P15 P16 P17 P19 P27 P28 : Point)
    (L12 : Line)
    (C02 C22 C28 : Circle)
    (h00 : line_circle_intersection P28 L12 C28)
    (h01 : between P06 P19 P00)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : area_le P12 P13 P14 P15 P16 P17)
    (h04 : angle_bisector_line P28 P10 P16 P27 L12)
    : on_line P28 L12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0188
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0188

theorem v06_sealed_holdout_0189
    (P02 P03 P09 P10 P16 P19 P22 P23 P25 P29 P31 : Point)
    (C02 C06 : Circle)
    (h00 : equilateral P09 P02 P31)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : between P16 P09 P02)
    (h03 : midpoint P19 P22 P25)
    (h04 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    : equal_length P09 P02 P02 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0189
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0189

theorem v06_sealed_holdout_0190
    (P00 P03 P04 P07 P08 P09 P10 P12 P14 P15 P16 P19 P20 P23 P25 P27 P29 : Point)
    (L02 L12 : Line)
    (C22 : Circle)
    (h00 : length_sum P14 P19 P29 P09 P16 P23)
    (h01 : between P25 P00 P07)
    (h02 : angle_bisector_line P20 P04 P15 P27 L12)
    (h03 : line_circle_intersection P03 L02 C22)
    (h04 : area_le P29 P12 P27 P10 P25 P08)
    : length_sum P29 P09 P14 P19 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0190
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0190

theorem v06_sealed_holdout_0191
    (P00 P04 P05 P06 P09 P11 P13 P15 P16 P18 P19 P21 P27 P30 : Point)
    (L10 : Line)
    (C00 : Circle)
    (h00 : equal_length P11 P30 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : area_le P00 P09 P18 P27 P04 P13)
    (h03 : line_circle_intersection P19 L10 C00)
    (h04 : midpoint P04 P21 P06)
    : equal_length P11 P30 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0191
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0191

theorem v06_sealed_holdout_0192
    (P00 P01 P02 P03 P07 P08 P11 P12 P13 P17 P18 P19 P21 P23 P24 P29 P30 : Point)
    (C02 C18 : Circle)
    (h00 : area_eq P00 P02 P21 P01 P12 P23)
    (h01 : area_eq P01 P12 P23 P03 P13 P24)
    (h02 : directed_angle_eq_mod_pi P07 P18 P29 P08 P19 P30)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : between P11 P30 P17)
    : area_eq P00 P02 P21 P03 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0192
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0192

theorem v06_sealed_holdout_0193
    (P01 P05 P07 P11 P13 P15 P16 P19 P27 P30 : Point)
    (L08 L17 L26 : Line)
    (C13 C20 : Circle)
    (h00 : equal_length P13 P30 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : line_circle_intersection P07 L17 C13)
    (h03 : line_circle_intersection P19 L26 C20)
    (h04 : angle_bisector_line P01 P11 P16 P27 L08)
    : equal_length P13 P30 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0193
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0193

theorem v06_sealed_holdout_0194
    (P02 P03 P07 P09 P12 P13 P16 P19 P20 P21 P22 P25 P26 P27 P28 P30 P31 : Point)
    (L10 : Line)
    (C06 : Circle)
    (h00 : tangent_chord_angle P26 P30 P25 L10 C06)
    (h01 : area_le P16 P09 P02 P27 P20 P13)
    (h02 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    (h03 : between P22 P03 P16)
    (h04 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    : on_circle P25 C06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0194
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0194

theorem v06_sealed_holdout_0195
    (P03 P04 P08 P09 P11 P13 P14 P16 P18 P19 P23 P26 P27 P30 P31 : Point)
    (L00 L04 L10 : Line)
    (C08 : Circle)
    (h00 : angle_bisector_line P31 P16 P23 P03 L04)
    (h01 : area_le P23 P18 P13 P08 P03 P30)
    (h02 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    (h03 : line_circle_intersection P19 L10 C08)
    (h04 : angle_bisector_line P03 P11 P16 P27 L00)
    : angle_bisector P31 P16 P23 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0195
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0195

theorem v06_sealed_holdout_0196
    (P03 P04 P07 P08 P11 P15 P16 P19 P23 P24 P25 P27 P31 : Point)
    (L12 L18 : Line)
    (C02 C18 C22 : Circle)
    (h00 : directed_angle_eq_mod_pi P08 P23 P03 P15 P24 P31)
    (h01 : directed_angle_eq_mod_pi P15 P24 P31 P07 P16 P25)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : line_circle_intersection P03 L18 C18)
    (h04 : angle_bisector_line P04 P11 P16 P27 L12)
    : directed_angle_eq_mod_pi P08 P23 P03 P07 P16 P25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0196
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0196

theorem v06_sealed_holdout_0197
    (P02 P04 P05 P07 P08 P09 P10 P11 P14 P16 P17 P20 P21 P23 P25 P27 P29 P30 P31 : Point)
    (h00 : directed_angle_eq_mod_2pi P29 P27 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : between P10 P31 P20)
    (h03 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h04 : directed_angle_eq_mod_pi P14 P11 P08 P05 P02 P31)
    : directed_angle_eq_mod_2pi P29 P27 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0197
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0197

theorem v06_sealed_holdout_0198
    (P01 P03 P05 P06 P07 P08 P10 P11 P15 P16 P23 P24 P25 P26 P27 P31 : Point)
    (L04 L08 : Line)
    (h00 : directed_angle_eq_mod_pi P10 P23 P03 P15 P24 P31)
    (h01 : directed_angle_eq_mod_pi P15 P24 P31 P07 P16 P25)
    (h02 : midpoint P15 P26 P05)
    (h03 : angle_bisector_line P01 P08 P16 P27 L08)
    (h04 : angle_bisector_line P06 P11 P16 P27 L04)
    : directed_angle_eq_mod_pi P10 P23 P03 P07 P16 P25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0198
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0198

theorem v06_sealed_holdout_0199
    (P02 P03 P07 P09 P10 P11 P16 P17 P21 P24 P25 P27 P28 P30 P31 : Point)
    (L16 : Line)
    (h00 : directed_angle_eq_mod_2pi P31 P27 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : directed_angle_eq_mod_pi P24 P17 P10 P03 P28 P21)
    (h03 : midpoint P25 P16 P07)
    (h04 : angle_bisector_line P07 P11 P16 P27 L16)
    : directed_angle_eq_mod_2pi P31 P27 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0199
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0199

theorem v06_sealed_holdout_0200
    (P00 P03 P04 P06 P08 P09 P10 P11 P12 P14 P15 P18 P19 P20 P25 P26 P27 P29 P31 : Point)
    (C07 : Circle)
    (h00 : circle_through_three_noncollinear_points P20 P06 P15 C07)
    (h01 : area_le P26 P31 P04 P09 P14 P19)
    (h02 : area_le P29 P12 P27 P10 P25 P08)
    (h03 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    (h04 : directed_angle_eq_mod_pi P03 P06 P09 P12 P15 P18)
    : triangle_pred P20 P06 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0200
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0200

theorem v06_sealed_holdout_0201
    (P01 P02 P03 P05 P06 P07 P08 P09 P15 P27 P29 P31 : Point)
    (L02 L16 : Line)
    (C22 : Circle)
    (h00 : equilateral P09 P06 P05)
    (h01 : midpoint P01 P08 P15)
    (h02 : angle_bisector_line P31 P05 P15 P27 L16)
    (h03 : between P07 P02 P29)
    (h04 : line_circle_intersection P03 L02 C22)
    : triangle_pred P09 P06 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0201
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0201

theorem v06_sealed_holdout_0202
    (P00 P02 P03 P05 P06 P08 P11 P14 P15 P17 P22 P24 P27 P31 : Point)
    (L18 L28 : Line)
    (C10 C21 : Circle)
    (h00 : circle_through_three_noncollinear_points P22 P06 P15 C21)
    (h01 : line_circle_intersection P03 L18 C10)
    (h02 : angle_bisector_line P00 P05 P15 P27 L28)
    (h03 : area_le P14 P11 P08 P05 P02 P31)
    (h04 : between P17 P24 P31)
    : triangle_pred P22 P06 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0202
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0202

theorem v06_sealed_holdout_0203
    (P01 P03 P05 P06 P08 P10 P11 P16 P19 P24 P27 P28 : Point)
    (L02 L04 L26 : Line)
    (C06 C20 : Circle)
    (h00 : equilateral P11 P06 P05)
    (h01 : line_circle_intersection P19 L26 C20)
    (h02 : line_circle_intersection P03 L02 C06)
    (h03 : angle_bisector_line P06 P08 P16 P27 L04)
    (h04 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    : triangle_pred P11 P06 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0203
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0203

theorem v06_sealed_holdout_0204
    (P00 P01 P02 P05 P06 P07 P11 P12 P15 P16 P25 P27 P28 P29 P30 P31 : Point)
    (L12 L24 : Line)
    (h00 : equilateral P12 P06 P05)
    (h01 : angle_bisector_line P29 P02 P15 P27 L24)
    (h02 : between P25 P16 P07)
    (h03 : area_le P28 P29 P30 P31 P00 P01)
    (h04 : angle_bisector_line P12 P11 P16 P27 L12)
    : triangle_pred P12 P06 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0204
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0204

theorem v06_sealed_holdout_0205
    (P00 P02 P03 P04 P07 P11 P12 P17 P18 P19 P22 P25 P27 P29 : Point)
    (L26 : Line)
    (C12 C18 C26 : Circle)
    (RF08 : Reflection)
    (h00 : area_le P02 P07 P12 P17 P22 P27)
    (h01 : midpoint P29 P12 P27)
    (h02 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    (h03 : line_circle_intersection P19 L26 C12)
    (h04 : circle_circle_intersection P03 C26 C18)
    : reflection_image RF08 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0205
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0205

theorem v06_sealed_holdout_0206
    (P02 P05 P09 P10 P11 P12 P13 P15 P16 P19 P20 P23 P27 P28 P30 P31 : Point)
    (L16 L26 : Line)
    (C04 : Circle)
    (HOM05 : Homothety)
    (h00 : directed_angle_eq_mod_pi P09 P16 P23 P30 P05 P12)
    (h01 : angle_bisector_line P31 P02 P15 P27 L16)
    (h02 : line_circle_intersection P19 L26 C04)
    (h03 : midpoint P10 P15 P20)
    (h04 : midpoint P13 P28 P11)
    : homothety_image HOM05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0206
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0206

theorem v06_sealed_holdout_0207
    (P04 P05 P08 P10 P11 P14 P15 P17 P20 P22 P23 P24 P30 P31 : Point)
    (L03 : Line)
    (C27 : Circle)
    (INV06 : Inversion)
    (h00 : line_circle_intersection P15 L03 C27)
    (h01 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h02 : midpoint P14 P11 P08)
    (h03 : between P17 P24 P31)
    (h04 : midpoint P20 P05 P22)
    : inversion_image INV06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0207
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0207

theorem v06_sealed_holdout_0208
    (P03 P06 P07 P16 P17 P18 P19 P20 P21 P27 P28 : Point)
    (L26 : Line)
    (C02 C10 C18 C22 C28 : Circle)
    (SP11 : SpiralSimilarity)
    (h00 : circle_circle_intersection P27 C22 C10)
    (h01 : area_le P18 P07 P28 P17 P06 P27)
    (h02 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : line_circle_intersection P19 L26 C28)
    : spiral_similarity_center SP11 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0208
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0208

theorem v06_sealed_holdout_0209
    (P02 P05 P06 P08 P12 P13 P19 P23 P27 P29 P31 : Point)
    (L28 : Line)
    (h00 : P05 = P08)
    (h01 : P06 = P19)
    (h02 : P27 = P31)
    (h03 : angle_bisector_line P29 P12 P31 P13 L28)
    (h04 : midpoint P02 P23 P12)
    : rotation_preserves_collinear P05 P06 P27 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0209
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0209

theorem v06_sealed_holdout_0210
    (P00 P05 P06 P09 P14 P18 P19 P23 P24 P25 P28 : Point)
    (L26 : Line)
    (C12 C23 : Circle)
    (h00 : circle_with_center_through_point P14 P24 C23)
    (h01 : between P00 P25 P18)
    (h02 : line_circle_intersection P19 L26 C12)
    (h03 : midpoint P06 P19 P00)
    (h04 : area_le P09 P00 P23 P14 P05 P28)
    : on_circle P24 C23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0210
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0210

theorem v06_sealed_holdout_0211
    (P02 P03 P05 P07 P09 P11 P13 P14 P15 P19 P24 P26 P27 P28 P29 P30 : Point)
    (L08 : Line)
    (C02 C05 C18 : Circle)
    (h00 : circle_through_three_noncollinear_points P03 P27 P30 C05)
    (h01 : area_le P07 P02 P29 P24 P19 P14)
    (h02 : angle_bisector_line P09 P05 P15 P27 L08)
    (h03 : area_le P13 P28 P11 P26 P09 P24)
    (h04 : circle_circle_intersection P03 C02 C18)
    : on_circle P03 C05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0211
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0211

theorem v06_sealed_holdout_0212
    (P02 P03 P05 P08 P11 P13 P14 P15 P16 P18 P19 P23 P27 P30 P31 : Point)
    (L10 L16 L21 : Line)
    (C00 C29 : Circle)
    (h00 : line_circle_intersection P08 L21 C29)
    (h01 : directed_angle_eq_mod_pi P14 P11 P08 P05 P02 P31)
    (h02 : line_circle_intersection P19 L10 C00)
    (h03 : angle_bisector_line P15 P08 P16 P27 L16)
    (h04 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    : on_circle P08 C29 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0212
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0212

theorem v06_sealed_holdout_0213
    (P01 P05 P10 P11 P16 P19 P20 P21 P24 P27 : Point)
    (L24 : Line)
    (C02 C12 C30 : Circle)
    (h00 : chord P05 P24 C12)
    (h01 : between P21 P20 P19)
    (h02 : between P24 P01 P10)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : angle_bisector_line P21 P11 P16 P27 L24)
    : on_circle P05 C12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0213
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0213

theorem v06_sealed_holdout_0214
    (P00 P01 P02 P03 P04 P05 P08 P10 P11 P12 P17 P21 P22 P23 P26 P27 P31 : Point)
    (L03 : Line)
    (C20 : Circle)
    (h00 : line_circle_intersection P27 L03 C20)
    (h01 : between P31 P10 P21)
    (h02 : area_le P02 P23 P12 P01 P22 P11)
    (h03 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    (h04 : area_le P08 P17 P26 P03 P12 P21)
    : on_line P27 L03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0214
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0214

theorem v06_sealed_holdout_0215
    (P00 P03 P06 P09 P12 P13 P14 P15 P16 P17 P23 : Point)
    (L01 : Line)
    (C18 C20 C26 : Circle)
    (h00 : line_circle_intersection P23 L01 C20)
    (h01 : midpoint P03 P06 P09)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : midpoint P09 P00 P23)
    (h04 : area_le P12 P13 P14 P15 P16 P17)
    : on_line P23 L01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0215
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0215

theorem v06_sealed_holdout_0216
    (P02 P03 P09 P10 P11 P12 P13 P16 P20 P23 P24 P26 P27 P28 : Point)
    (L21 L28 : Line)
    (C10 C18 : Circle)
    (h00 : altitude P12 P10 P11 P23 L21)
    (h01 : circle_circle_intersection P03 C10 C18)
    (h02 : area_le P13 P28 P11 P26 P09 P24)
    (h03 : area_le P16 P09 P02 P27 P20 P13)
    (h04 : angle_bisector_line P24 P11 P16 P27 L28)
    : on_line P11 L21 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0216
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0216

theorem v06_sealed_holdout_0217
    (P01 P02 P03 P05 P07 P09 P10 P13 P15 P17 P19 P20 P22 P24 P27 P29 : Point)
    (L08 L20 L26 : Line)
    (C04 C10 C18 : Circle)
    (h00 : angle_bisector_line P01 P13 P17 P29 L08)
    (h01 : angle_bisector_line P10 P02 P15 P27 L20)
    (h02 : area_le P20 P05 P22 P07 P24 P09)
    (h03 : line_circle_intersection P19 L26 C04)
    (h04 : circle_circle_intersection P03 C10 C18)
    : on_line P01 L08 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0217
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0217

theorem v06_sealed_holdout_0218
    (P01 P05 P08 P10 P15 P16 P19 P21 P24 P26 P27 : Point)
    (L14 L24 L28 : Line)
    (C02 C12 C22 : Circle)
    (h00 : line_circle_intersection P26 L14 C12)
    (h01 : midpoint P24 P01 P10)
    (h02 : angle_bisector_line P16 P05 P15 P27 L28)
    (h03 : angle_bisector_line P21 P08 P16 P27 L24)
    (h04 : circle_circle_intersection P19 C22 C02)
    : on_line P26 L14 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0218
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0218

theorem v06_sealed_holdout_0219
    (P02 P03 P07 P10 P11 P12 P16 P19 P21 P23 P27 P28 P31 : Point)
    (L00 L10 : Line)
    (C24 : Circle)
    (h00 : equilateral P07 P03 P31)
    (h01 : between P31 P10 P21)
    (h02 : midpoint P02 P23 P12)
    (h03 : line_circle_intersection P19 L10 C24)
    (h04 : angle_bisector_line P27 P11 P16 P28 L00)
    : equal_length P07 P03 P03 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0219
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0219

theorem v06_sealed_holdout_0220
    (P00 P05 P08 P09 P11 P12 P14 P15 P16 P17 P20 P23 P26 P27 P29 : Point)
    (L16 : Line)
    (h00 : length_sum P12 P20 P29 P09 P16 P23)
    (h01 : directed_angle_eq_mod_pi P11 P14 P17 P20 P23 P26)
    (h02 : between P09 P00 P23)
    (h03 : angle_bisector_line P23 P08 P16 P27 L16)
    (h04 : midpoint P15 P26 P05)
    : length_sum P29 P09 P12 P20 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0220
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0220

theorem v06_sealed_holdout_0221
    (P05 P09 P12 P15 P16 P19 P22 P23 P25 P27 P29 P31 : Point)
    (L21 L24 : Line)
    (C09 : Circle)
    (h00 : equal_length P09 P31 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : line_circle_intersection P23 L21 C09)
    (h03 : midpoint P19 P22 P25)
    (h04 : angle_bisector_line P29 P12 P16 P27 L24)
    : equal_length P09 P31 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0221
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0221

theorem v06_sealed_holdout_0222
    (P01 P02 P03 P04 P12 P13 P19 P21 P23 P24 P26 P30 P31 : Point)
    (L10 : Line)
    (C06 C08 C18 : Circle)
    (h00 : area_eq P30 P02 P21 P01 P12 P23)
    (h01 : area_eq P01 P12 P23 P03 P13 P24)
    (h02 : circle_circle_intersection P03 C06 C18)
    (h03 : midpoint P26 P31 P04)
    (h04 : line_circle_intersection P19 L10 C08)
    : area_eq P30 P02 P21 P03 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0222
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0222

theorem v06_sealed_holdout_0223
    (P01 P04 P05 P06 P08 P11 P12 P13 P15 P16 P21 P23 P25 P27 P31 : Point)
    (L12 : Line)
    (h00 : equal_length P11 P31 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : angle_bisector_line P11 P12 P31 P13 L12)
    (h03 : between P01 P08 P15)
    (h04 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    : equal_length P11 P31 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0223
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0223

theorem v06_sealed_holdout_0224
    (P01 P02 P03 P04 P05 P08 P11 P14 P16 P19 P24 P27 P28 P31 : Point)
    (L00 L08 L26 : Line)
    (C28 : Circle)
    (h00 : angle_bisector_line P01 P16 P24 P03 L08)
    (h01 : midpoint P05 P04 P03)
    (h02 : angle_bisector_line P27 P04 P16 P28 L00)
    (h03 : line_circle_intersection P19 L26 C28)
    (h04 : directed_angle_eq_mod_pi P14 P11 P08 P05 P02 P31)
    : angle_bisector P01 P16 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0224
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0224

theorem v06_sealed_holdout_0225
    (P00 P03 P05 P06 P07 P09 P12 P13 P14 P15 P16 P17 P18 P23 P26 P27 P28 P29 : Point)
    (L06 : Line)
    (h00 : angle_bisector_line P29 P17 P23 P03 L06)
    (h01 : midpoint P09 P00 P23)
    (h02 : between P12 P13 P14)
    (h03 : area_le P15 P26 P05 P16 P27 P06)
    (h04 : directed_angle_eq_mod_pi P18 P07 P28 P17 P06 P27)
    : angle_bisector P29 P17 P23 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0225
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0225

theorem v06_sealed_holdout_0226
    (P03 P06 P07 P12 P15 P16 P19 P21 P23 P24 P25 P30 P31 : Point)
    (C02 C18 C26 C30 : Circle)
    (h00 : directed_angle_eq_mod_pi P06 P24 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P25)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    : directed_angle_eq_mod_pi P06 P24 P03 P07 P16 P25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0226
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0226

theorem v06_sealed_holdout_0227
    (P00 P02 P07 P08 P09 P10 P12 P13 P15 P16 P17 P18 P21 P25 P27 P28 P29 P30 : Point)
    (h00 : directed_angle_eq_mod_2pi P27 P28 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : directed_angle_eq_mod_pi P28 P13 P30 P15 P00 P17)
    (h03 : directed_angle_eq_mod_pi P29 P12 P27 P10 P25 P08)
    (h04 : midpoint P00 P25 P18)
    : directed_angle_eq_mod_2pi P27 P28 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0227
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0227

theorem v06_sealed_holdout_0228
    (P01 P02 P03 P07 P08 P09 P14 P15 P16 P19 P23 P24 P25 P27 P29 P31 : Point)
    (L16 : Line)
    (h00 : directed_angle_eq_mod_pi P08 P24 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P25)
    (h02 : midpoint P01 P08 P15)
    (h03 : angle_bisector_line P31 P09 P16 P27 L16)
    (h04 : area_le P07 P02 P29 P24 P19 P14)
    : directed_angle_eq_mod_pi P08 P24 P03 P07 P16 P25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0228
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0228

theorem v06_sealed_holdout_0229
    (P00 P02 P03 P07 P09 P16 P21 P23 P25 P27 P28 P29 P30 : Point)
    (L02 L28 : Line)
    (C06 C14 C30 : Circle)
    (h00 : directed_angle_eq_mod_2pi P29 P28 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : circle_circle_intersection P23 C30 C06)
    (h03 : angle_bisector_line P00 P09 P16 P27 L28)
    (h04 : line_circle_intersection P03 L02 C14)
    : directed_angle_eq_mod_2pi P29 P28 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0229
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0229

theorem v06_sealed_holdout_0230
    (P07 P12 P13 P14 P15 P16 P17 P18 P19 P20 P21 P28 : Point)
    (C02 C14 C25 : Circle)
    (h00 : circle_through_three_noncollinear_points P18 P07 P16 C25)
    (h01 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : between P18 P07 P28)
    (h04 : area_le P21 P20 P19 P18 P17 P16)
    : triangle_pred P18 P07 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0230
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0230

theorem v06_sealed_holdout_0231
    (P02 P03 P05 P06 P07 P12 P16 P19 P22 P25 P27 P28 P31 : Point)
    (L10 L16 : Line)
    (C16 C18 C26 : Circle)
    (h00 : equilateral P07 P06 P05)
    (h01 : area_le P19 P22 P25 P28 P31 P02)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : line_circle_intersection P19 L10 C16)
    (h04 : angle_bisector_line P07 P12 P16 P27 L16)
    : triangle_pred P07 P06 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0231
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0231

theorem v06_sealed_holdout_0232
    (P03 P04 P06 P07 P09 P12 P15 P16 P18 P19 P20 P26 P31 : Point)
    (L10 L18 : Line)
    (C07 C08 C26 : Circle)
    (h00 : circle_through_three_noncollinear_points P20 P07 P16 C07)
    (h01 : between P26 P31 P04)
    (h02 : line_circle_intersection P19 L10 C08)
    (h03 : line_circle_intersection P03 L18 C26)
    (h04 : area_le P03 P06 P09 P12 P15 P18)
    : triangle_pred P20 P07 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0232
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0232

theorem v06_sealed_holdout_0233
    (P02 P05 P06 P07 P09 P12 P14 P15 P16 P19 P24 P27 P29 P31 : Point)
    (L08 L10 L16 : Line)
    (C00 : Circle)
    (h00 : equilateral P09 P07 P05)
    (h01 : line_circle_intersection P19 L10 C00)
    (h02 : angle_bisector_line P31 P06 P15 P27 L16)
    (h03 : area_le P07 P02 P29 P24 P19 P14)
    (h04 : angle_bisector_line P09 P12 P16 P27 L08)
    : triangle_pred P09 P07 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0233
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0233

theorem v06_sealed_holdout_0234
    (P03 P04 P05 P07 P08 P10 P11 P12 P16 P17 P23 P26 P27 P30 : Point)
    (L02 L20 : Line)
    (C14 : Circle)
    (h00 : equilateral P10 P07 P05)
    (h01 : between P08 P17 P26)
    (h02 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h03 : line_circle_intersection P03 L02 C14)
    (h04 : angle_bisector_line P10 P12 P16 P27 L20)
    : triangle_pred P10 P07 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0234
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0234

theorem v06_sealed_holdout_0235
    (P01 P05 P06 P07 P10 P15 P16 P18 P19 P20 P21 P24 P26 P27 P28 P31 : Point)
    (L07 : Line)
    (C23 : Circle)
    (RF26 : Reflection)
    (h00 : line_circle_intersection P31 L07 C23)
    (h01 : area_le P15 P26 P05 P16 P27 P06)
    (h02 : midpoint P18 P07 P28)
    (h03 : between P21 P20 P19)
    (h04 : area_le P24 P01 P10 P19 P28 P05)
    : reflection_image RF26 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0235
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0235

theorem v06_sealed_holdout_0236
    (P00 P01 P03 P11 P19 P28 P29 P30 P31 : Point)
    (L10 : Line)
    (C02 C14 C16 C18 C22 C26 : Circle)
    (HOM19 : Homothety)
    (h00 : circle_circle_intersection P11 C22 C26)
    (h01 : circle_circle_intersection P03 C26 C18)
    (h02 : line_circle_intersection P19 L10 C16)
    (h03 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    (h04 : circle_circle_intersection P19 C14 C02)
    : homothety_image HOM19 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0236
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0236

theorem v06_sealed_holdout_0237
    (P03 P08 P09 P13 P14 P16 P19 P25 P27 P31 : Point)
    (L28 : Line)
    (C02 C06 C18 C26 : Circle)
    (INV16 : Inversion)
    (h00 : angle_bisector_line P25 P13 P31 P14 L28)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : angle_bisector_line P08 P09 P16 P27 L28)
    (h04 : circle_circle_intersection P03 C26 C18)
    : inversion_image INV16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0237
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0237

theorem v06_sealed_holdout_0238
    (P03 P04 P06 P09 P11 P13 P15 P16 P23 P27 P28 P31 : Point)
    (L02 L12 L16 : Line)
    (C22 : Circle)
    (SP17 : SpiralSimilarity)
    (h00 : midpoint P09 P16 P23)
    (h01 : angle_bisector_line P31 P03 P15 P27 L16)
    (h02 : angle_bisector_line P04 P06 P15 P27 L12)
    (h03 : line_circle_intersection P03 L02 C22)
    (h04 : between P13 P28 P11)
    : spiral_similarity_center SP17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0238
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0238

theorem v06_sealed_holdout_0239
    (P02 P03 P05 P07 P08 P16 P19 P20 P22 P25 P27 P31 : Point)
    (h00 : P03 = P08)
    (h01 : P07 = P19)
    (h02 : P27 = P31)
    (h03 : between P16 P25 P02)
    (h04 : midpoint P20 P05 P22)
    : rotation_preserves_collinear P03 P07 P27 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0239
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0239

theorem v06_sealed_holdout_0240
    (P01 P03 P06 P07 P12 P14 P15 P17 P18 P25 P27 P28 : Point)
    (L04 : Line)
    (C02 C18 C27 : Circle)
    (h00 : circle_with_center_through_point P12 P25 C27)
    (h01 : directed_angle_eq_mod_pi P18 P07 P28 P17 P06 P27)
    (h02 : angle_bisector_line P06 P07 P15 P27 L04)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : between P27 P14 P01)
    : on_circle P25 C27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0240
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0240

theorem v06_sealed_holdout_0241
    (P00 P01 P02 P07 P10 P11 P12 P16 P21 P22 P23 P25 P28 P29 P30 P31 : Point)
    (C07 : Circle)
    (h00 : circle_through_three_noncollinear_points P01 P28 P30 C07)
    (h01 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h02 : between P28 P29 P30)
    (h03 : area_le P31 P10 P21 P00 P11 P22)
    (h04 : midpoint P02 P23 P12)
    : on_circle P01 C07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0241
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0241

theorem v06_sealed_holdout_0242
    (P00 P03 P04 P05 P06 P09 P11 P14 P18 P19 P23 P25 P28 P29 : Point)
    (L21 : Line)
    (C11 : Circle)
    (h00 : line_circle_intersection P06 L21 C11)
    (h01 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    (h02 : midpoint P03 P06 P09)
    (h03 : midpoint P06 P19 P00)
    (h04 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    : on_circle P06 C11 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0242
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0242

theorem v06_sealed_holdout_0243
    (P02 P03 P07 P10 P11 P13 P14 P15 P19 P20 P24 P25 P28 P29 P30 : Point)
    (L18 : Line)
    (C20 C26 : Circle)
    (h00 : chord P03 P25 C20)
    (h01 : directed_angle_eq_mod_pi P07 P02 P29 P24 P19 P14)
    (h02 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    (h03 : midpoint P13 P28 P11)
    (h04 : line_circle_intersection P03 L18 C26)
    : on_circle P03 C20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0243
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0243

theorem v06_sealed_holdout_0244
    (P02 P03 P08 P10 P11 P16 P17 P20 P25 P27 P28 : Point)
    (L05 L08 L12 L18 L20 : Line)
    (C04 C18 : Circle)
    (h00 : line_circle_intersection P25 L05 C04)
    (h01 : angle_bisector_line P10 P02 P16 P27 L20)
    (h02 : line_circle_intersection P03 L18 C18)
    (h03 : angle_bisector_line P20 P08 P17 P28 L12)
    (h04 : angle_bisector_line P25 P11 P17 P28 L08)
    : on_line P25 L05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0244
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0244

theorem v06_sealed_holdout_0245
    (P01 P05 P07 P10 P14 P15 P18 P19 P20 P21 P24 P26 P27 P28 P30 : Point)
    (L03 : Line)
    (C04 : Circle)
    (h00 : line_circle_intersection P21 L03 C04)
    (h01 : midpoint P21 P20 P19)
    (h02 : area_le P24 P01 P10 P19 P28 P05)
    (h03 : area_le P27 P14 P01 P20 P07 P26)
    (h04 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    : on_line P21 L03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0245
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0245

theorem v06_sealed_holdout_0246
    (P03 P10 P11 P12 P19 P21 P23 P28 P29 P30 P31 : Point)
    (L27 : Line)
    (C02 C06 C10 C18 : Circle)
    (h00 : altitude P10 P11 P12 P23 L27)
    (h01 : midpoint P28 P29 P30)
    (h02 : midpoint P31 P10 P21)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : circle_circle_intersection P19 C06 C02)
    : on_line P12 L27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0246
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0246

theorem v06_sealed_holdout_0247
    (P00 P03 P05 P06 P07 P08 P09 P13 P14 P15 P17 P19 P23 P26 P27 P28 P29 P31 : Point)
    (L12 L28 : Line)
    (C18 C19 : Circle)
    (h00 : angle_bisector_line P31 P14 P17 P29 L12)
    (h01 : angle_bisector_line P08 P03 P15 P27 L28)
    (h02 : area_le P06 P19 P00 P13 P26 P07)
    (h03 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h04 : circle_circle_intersection P03 C18 C19)
    : on_line P31 L12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0247
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0247

theorem v06_sealed_holdout_0248
    (P02 P09 P10 P11 P13 P15 P16 P19 P20 P22 P24 P25 P26 P27 P28 P31 : Point)
    (L16 : Line)
    (C28 : Circle)
    (h00 : line_circle_intersection P24 L16 C28)
    (h01 : midpoint P10 P15 P20)
    (h02 : directed_angle_eq_mod_pi P13 P28 P11 P26 P09 P24)
    (h03 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    (h04 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    : on_line P24 L16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0248
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0248

theorem v06_sealed_holdout_0249
    (P04 P05 P06 P07 P09 P12 P13 P16 P17 P18 P20 P22 P23 P24 P25 P27 P31 : Point)
    (L08 : Line)
    (h00 : equilateral P05 P04 P31)
    (h01 : area_le P17 P24 P31 P06 P13 P20)
    (h02 : area_le P20 P05 P22 P07 P24 P09)
    (h03 : between P23 P18 P13)
    (h04 : angle_bisector_line P25 P12 P16 P27 L08)
    : equal_length P05 P04 P04 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0249
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0249

theorem v06_sealed_holdout_0250
    (P01 P09 P10 P14 P15 P16 P18 P19 P21 P23 P24 P27 P29 P30 : Point)
    (C02 C06 C22 : Circle)
    (h00 : length_sum P10 P21 P29 P09 P16 P23)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : between P27 P14 P01)
    (h03 : area_le P30 P27 P24 P21 P18 P15)
    (h04 : circle_circle_intersection P19 C22 C02)
    : length_sum P29 P09 P10 P21 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0250
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0250

theorem v06_sealed_holdout_0251
    (P00 P03 P05 P07 P08 P12 P13 P14 P15 P16 P17 P19 P21 P26 P27 P31 : Point)
    (L10 L12 : Line)
    (C24 : Circle)
    (h00 : equal_length P07 P00 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : angle_bisector_line P07 P13 P31 P14 L12)
    (h03 : line_circle_intersection P19 L10 C24)
    (h04 : area_le P08 P17 P26 P03 P12 P21)
    : equal_length P07 P00 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0251
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0251

theorem v06_sealed_holdout_0252
    (P01 P02 P03 P05 P06 P11 P12 P13 P14 P15 P16 P17 P21 P23 P24 P26 P27 P28 : Point)
    (L18 : Line)
    (C02 : Circle)
    (h00 : area_eq P28 P03 P21 P01 P12 P23)
    (h01 : area_eq P01 P12 P23 P02 P13 P24)
    (h02 : midpoint P11 P14 P17)
    (h03 : line_circle_intersection P03 L18 C02)
    (h04 : area_le P15 P26 P05 P16 P27 P06)
    : area_eq P28 P03 P21 P02 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0252
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0252

theorem v06_sealed_holdout_0253
    (P00 P03 P05 P09 P15 P16 P18 P19 P22 P23 P25 P27 P28 : Point)
    (h00 : equal_length P09 P00 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : between P18 P23 P28)
    (h03 : midpoint P19 P22 P25)
    (h04 : between P22 P03 P16)
    : equal_length P09 P00 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0253
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0253

theorem v06_sealed_holdout_0254
    (P03 P04 P09 P14 P17 P19 P24 P26 P31 : Point)
    (L10 L26 : Line)
    (C02 C04 C08 C18 : Circle)
    (h00 : angle_bisector_line P31 P17 P24 P03 L10)
    (h01 : line_circle_intersection P19 L26 C04)
    (h02 : area_le P26 P31 P04 P09 P14 P19)
    (h03 : line_circle_intersection P19 L10 C08)
    (h04 : circle_circle_intersection P03 C02 C18)
    : angle_bisector P31 P17 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0254
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0254

theorem v06_sealed_holdout_0255
    (P03 P04 P06 P08 P09 P15 P16 P18 P21 P23 P25 P26 P27 : Point)
    (L02 L08 L20 L28 : Line)
    (C14 : Circle)
    (h00 : angle_bisector_line P27 P18 P23 P03 L08)
    (h01 : angle_bisector_line P16 P03 P15 P27 L28)
    (h02 : line_circle_intersection P03 L02 C14)
    (h03 : angle_bisector_line P26 P09 P16 P27 L20)
    (h04 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    : angle_bisector P27 P18 P23 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0255
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0255

theorem v06_sealed_holdout_0256
    (P03 P04 P05 P07 P09 P15 P16 P19 P23 P24 P25 P27 P28 P31 : Point)
    (L00 : Line)
    (C02 C30 : Circle)
    (h00 : directed_angle_eq_mod_pi P04 P25 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : between P05 P04 P03)
    (h03 : angle_bisector_line P27 P09 P16 P28 L00)
    (h04 : circle_circle_intersection P19 C30 C02)
    : directed_angle_eq_mod_pi P04 P25 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0256
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0256

theorem v06_sealed_holdout_0257
    (P02 P03 P05 P07 P09 P15 P16 P21 P25 P26 P28 P30 : Point)
    (C10 C18 C22 C30 : Circle)
    (h00 : directed_angle_eq_mod_2pi P25 P28 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P26 P02)
    (h02 : circle_circle_intersection P07 C30 C22)
    (h03 : midpoint P15 P26 P05)
    (h04 : circle_circle_intersection P03 C10 C18)
    : directed_angle_eq_mod_2pi P25 P28 P09 P16 P26 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0257
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0257

theorem v06_sealed_holdout_0258
    (P02 P03 P06 P07 P12 P15 P16 P19 P21 P22 P23 P24 P25 P28 P30 P31 : Point)
    (h00 : directed_angle_eq_mod_pi P06 P25 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : area_le P19 P22 P25 P28 P31 P02)
    (h03 : between P22 P03 P16)
    (h04 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    : directed_angle_eq_mod_pi P06 P25 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0258
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0258

theorem v06_sealed_holdout_0259
    (P00 P02 P07 P09 P12 P13 P16 P18 P21 P25 P27 P28 P29 P30 : Point)
    (h00 : directed_angle_eq_mod_2pi P27 P29 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : midpoint P28 P13 P30)
    (h03 : midpoint P29 P12 P27)
    (h04 : between P00 P25 P18)
    : directed_angle_eq_mod_2pi P27 P29 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0259
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0259

theorem v06_sealed_holdout_0260
    (P03 P08 P16 P17 P19 P24 P27 P30 : Point)
    (L10 L18 L26 : Line)
    (C00 C04 C11 C18 : Circle)
    (h00 : circle_through_three_noncollinear_points P16 P08 P17 C11)
    (h01 : between P30 P27 P24)
    (h02 : line_circle_intersection P19 L10 C00)
    (h03 : line_circle_intersection P03 L18 C18)
    (h04 : line_circle_intersection P19 L26 C04)
    : triangle_pred P16 P08 P17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0260
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0260

theorem v06_sealed_holdout_0261
    (P00 P03 P05 P06 P07 P08 P10 P11 P12 P14 P16 P17 P19 P21 P26 P27 : Point)
    (L28 : Line)
    (C02 C06 : Circle)
    (h00 : equilateral P05 P07 P06)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : area_le P08 P17 P26 P03 P12 P21)
    (h03 : angle_bisector_line P00 P10 P16 P27 L28)
    (h04 : midpoint P14 P11 P08)
    : triangle_pred P05 P07 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0261
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0261

theorem v06_sealed_holdout_0262
    (P03 P06 P07 P08 P16 P17 P18 P19 P27 P28 : Point)
    (L26 : Line)
    (C02 C06 C18 C19 C20 C25 : Circle)
    (h00 : circle_through_three_noncollinear_points P18 P08 P16 C25)
    (h01 : circle_circle_intersection P03 C18 C19)
    (h02 : line_circle_intersection P19 L26 C20)
    (h03 : directed_angle_eq_mod_pi P18 P07 P28 P17 P06 P27)
    (h04 : circle_circle_intersection P19 C06 C02)
    : triangle_pred P18 P08 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0262
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0262

theorem v06_sealed_holdout_0263
    (P00 P01 P03 P05 P07 P08 P16 P19 P22 P25 P28 P29 P30 P31 : Point)
    (h00 : equilateral P07 P08 P05)
    (h01 : between P19 P22 P25)
    (h02 : midpoint P22 P03 P16)
    (h03 : midpoint P25 P16 P07)
    (h04 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    : triangle_pred P07 P08 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0263
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0263

theorem v06_sealed_holdout_0264
    (P03 P05 P08 P09 P10 P12 P15 P19 P25 P27 P29 : Point)
    (L08 L18 L26 : Line)
    (C12 C26 : Circle)
    (h00 : equilateral P08 P09 P05)
    (h01 : angle_bisector_line P25 P03 P15 P27 L08)
    (h02 : area_le P29 P12 P27 P10 P25 P08)
    (h03 : line_circle_intersection P03 L18 C26)
    (h04 : line_circle_intersection P19 L26 C12)
    : triangle_pred P08 P09 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0264
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0264

theorem v06_sealed_holdout_0265
    (P02 P03 P04 P06 P07 P13 P14 P15 P19 P21 P24 P26 P27 P29 P31 : Point)
    (L20 L28 : Line)
    (C10 C18 : Circle)
    (RF44 : Reflection)
    (h00 : angle_bisector_line P21 P14 P31 P13 L28)
    (h01 : angle_bisector_line P26 P03 P15 P27 L20)
    (h02 : between P04 P21 P06)
    (h03 : area_le P07 P02 P29 P24 P19 P14)
    (h04 : circle_circle_intersection P03 C10 C18)
    : reflection_image RF44 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0265
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0265

theorem v06_sealed_holdout_0266
    (P02 P03 P05 P06 P08 P11 P12 P13 P14 P17 P19 P20 P24 P31 : Point)
    (L26 : Line)
    (C02 C18 C28 : Circle)
    (HOM33 : Homothety)
    (h00 : midpoint P13 P12 P11)
    (h01 : circle_circle_intersection P03 C02 C18)
    (h02 : line_circle_intersection P19 L26 C28)
    (h03 : area_le P14 P11 P08 P05 P02 P31)
    (h04 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    : homothety_image HOM33 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0266
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0266

theorem v06_sealed_holdout_0267
    (P01 P05 P06 P07 P11 P13 P15 P16 P17 P18 P19 P20 P21 P22 P26 P27 : Point)
    (L00 L08 : Line)
    (INV26 : Inversion)
    (h00 : between P20 P21 P22)
    (h01 : directed_angle_eq_mod_pi P15 P26 P05 P16 P27 P06)
    (h02 : angle_bisector_line P01 P07 P16 P27 L08)
    (h03 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    (h04 : angle_bisector_line P11 P13 P16 P27 L00)
    : inversion_image INV26 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0267
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0267

theorem v06_sealed_holdout_0268
    (P01 P03 P04 P07 P10 P12 P16 P19 P21 P22 P23 P25 P27 P29 P30 : Point)
    (L16 : Line)
    (C02 C14 : Circle)
    (SP23 : SpiralSimilarity)
    (h00 : area_le P27 P30 P01 P04 P07 P10)
    (h01 : area_le P22 P03 P16 P29 P10 P23)
    (h02 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h03 : angle_bisector_line P07 P10 P16 P27 L16)
    (h04 : circle_circle_intersection P19 C14 C02)
    : spiral_similarity_center SP23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0268
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0268

theorem v06_sealed_holdout_0269
    (P01 P02 P03 P07 P08 P12 P17 P19 P22 P27 P31 : Point)
    (C18 C26 : Circle)
    (h00 : P01 = P08)
    (h01 : P07 = P19)
    (h02 : P27 = P31)
    (h03 : directed_angle_eq_mod_pi P02 P07 P12 P17 P22 P27)
    (h04 : circle_circle_intersection P03 C26 C18)
    : rotation_preserves_collinear P01 P07 P27 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0269
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0269

theorem v06_sealed_holdout_0270
    (P02 P03 P07 P10 P19 P26 P29 : Point)
    (L10 : Line)
    (C08 C10 C18 C19 C31 : Circle)
    (h00 : circle_with_center_through_point P10 P26 C31)
    (h01 : circle_circle_intersection P03 C18 C19)
    (h02 : between P07 P02 P29)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : line_circle_intersection P19 L10 C08)
    : on_circle P26 C31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0270
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0270

theorem v06_sealed_holdout_0271
    (P03 P05 P06 P11 P13 P17 P20 P22 P24 P29 P30 P31 : Point)
    (C09 C18 C26 : Circle)
    (h00 : circle_through_three_noncollinear_points P31 P29 P30 C09)
    (h01 : midpoint P11 P30 P17)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : area_le P17 P24 P31 P06 P13 P20)
    (h04 : midpoint P20 P05 P22)
    : on_circle P31 C09 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0271
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0271

theorem v06_sealed_holdout_0272
    (P01 P04 P05 P07 P10 P13 P16 P17 P18 P19 P20 P21 P24 P27 P28 : Point)
    (L21 L28 : Line)
    (C25 : Circle)
    (h00 : line_circle_intersection P04 L21 C25)
    (h01 : between P18 P07 P28)
    (h02 : between P21 P20 P19)
    (h03 : area_le P24 P01 P10 P19 P28 P05)
    (h04 : angle_bisector_line P16 P13 P17 P27 L28)
    : on_circle P04 C25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0272
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0272

theorem v06_sealed_holdout_0273
    (P00 P01 P02 P03 P04 P10 P15 P21 P26 P27 P28 P29 P30 P31 : Point)
    (L20 : Line)
    (C10 C18 C28 : Circle)
    (h00 : chord P01 P26 C28)
    (h01 : angle_bisector_line P02 P04 P15 P27 L20)
    (h02 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    (h03 : midpoint P31 P10 P21)
    (h04 : circle_circle_intersection P03 C10 C18)
    : on_circle P01 C28 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0273
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0273

theorem v06_sealed_holdout_0274
    (P00 P03 P05 P06 P09 P12 P14 P17 P19 P23 P28 : Point)
    (L07 L16 : Line)
    (C20 : Circle)
    (h00 : line_circle_intersection P23 L07 C20)
    (h01 : between P03 P06 P09)
    (h02 : midpoint P06 P19 P00)
    (h03 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h04 : angle_bisector_line P23 P12 P17 P28 L16)
    : on_line P23 L07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0274
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0274

theorem v06_sealed_holdout_0275
    (P02 P07 P09 P10 P13 P14 P15 P16 P19 P20 P27 P29 : Point)
    (L04 L05 : Line)
    (C20 : Circle)
    (h00 : line_circle_intersection P19 L05 C20)
    (h01 : midpoint P07 P02 P29)
    (h02 : midpoint P10 P15 P20)
    (h03 : angle_bisector_line P14 P10 P16 P27 L04)
    (h04 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    : on_line P19 L05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0275
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0275

theorem v06_sealed_holdout_0276
    (P03 P05 P07 P08 P10 P11 P12 P13 P16 P18 P20 P22 P23 P27 : Point)
    (L01 L02 L20 : Line)
    (C14 : Circle)
    (h00 : altitude P08 P11 P12 P23 L01)
    (h01 : line_circle_intersection P03 L02 C14)
    (h02 : angle_bisector_line P10 P07 P16 P27 L20)
    (h03 : midpoint P20 P05 P22)
    (h04 : between P23 P18 P13)
    : on_line P12 L01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0276
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0276

theorem v06_sealed_holdout_0277
    (P01 P03 P14 P15 P17 P19 P27 P29 P30 : Point)
    (L16 : Line)
    (C02 C06 C18 C26 : Circle)
    (h00 : angle_bisector_line P29 P15 P17 P30 L16)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : midpoint P27 P14 P01)
    (h04 : circle_circle_intersection P03 C26 C18)
    : on_line P29 L16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0277
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0277

theorem v06_sealed_holdout_0278
    (P00 P01 P03 P04 P05 P10 P16 P17 P21 P22 P27 P28 P29 P30 P31 : Point)
    (L08 L18 : Line)
    (C12 : Circle)
    (h00 : line_circle_intersection P22 L18 C12)
    (h01 : area_le P28 P29 P30 P31 P00 P01)
    (h02 : midpoint P31 P10 P21)
    (h03 : angle_bisector_line P17 P10 P16 P27 L08)
    (h04 : midpoint P05 P04 P03)
    : on_line P22 L18 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0278
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0278

theorem v06_sealed_holdout_0279
    (P00 P03 P04 P06 P08 P12 P13 P14 P15 P16 P17 P19 P27 P31 : Point)
    (L10 L28 : Line)
    (C16 : Circle)
    (h00 : equilateral P03 P04 P31)
    (h01 : angle_bisector_line P08 P04 P15 P27 L28)
    (h02 : midpoint P06 P19 P00)
    (h03 : line_circle_intersection P19 L10 C16)
    (h04 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    : equal_length P03 P04 P04 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0279
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0279

theorem v06_sealed_holdout_0280
    (P02 P05 P08 P09 P10 P11 P13 P15 P16 P19 P22 P23 P25 P27 P28 P29 P31 : Point)
    (L00 : Line)
    (h00 : length_sum P08 P22 P29 P09 P16 P23)
    (h01 : midpoint P15 P10 P05)
    (h02 : midpoint P13 P28 P11)
    (h03 : angle_bisector_line P19 P10 P16 P27 L00)
    (h04 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    : length_sum P29 P09 P08 P22 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0280
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0280

theorem v06_sealed_holdout_0281
    (P01 P04 P05 P06 P09 P14 P15 P16 P19 P22 P26 P27 P31 : Point)
    (C02 C14 : Circle)
    (h00 : equal_length P05 P01 P15 P27)
    (h01 : equal_length P15 P27 P06 P16)
    (h02 : between P22 P19 P16)
    (h03 : circle_circle_intersection P19 C14 C02)
    (h04 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    : equal_length P05 P01 P06 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0281
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0281

theorem v06_sealed_holdout_0282
    (P01 P02 P04 P08 P12 P13 P15 P21 P23 P24 P25 P26 P27 P28 P29 P30 : Point)
    (h00 : area_eq P26 P04 P21 P01 P12 P23)
    (h01 : area_eq P01 P12 P23 P02 P13 P24)
    (h02 : area_le P29 P28 P27 P26 P25 P24)
    (h03 : midpoint P30 P27 P24)
    (h04 : between P01 P08 P15)
    : area_eq P26 P04 P21 P02 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0282
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0282

theorem v06_sealed_holdout_0283
    (P01 P03 P04 P05 P06 P07 P08 P09 P15 P16 P19 P27 : Point)
    (L10 L18 : Line)
    (C10 C24 : Circle)
    (h00 : equal_length P07 P01 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : directed_angle_eq_mod_pi P04 P05 P06 P07 P08 P09)
    (h03 : line_circle_intersection P19 L10 C24)
    (h04 : line_circle_intersection P03 L18 C10)
    : equal_length P07 P01 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0283
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0283

theorem v06_sealed_holdout_0284
    (P03 P07 P09 P12 P13 P14 P15 P16 P17 P18 P19 P24 P28 P29 : Point)
    (L12 : Line)
    (C02 C22 : Circle)
    (h00 : angle_bisector_line P29 P18 P24 P03 L12)
    (h01 : circle_circle_intersection P19 C22 C02)
    (h02 : area_le P12 P13 P14 P15 P16 P17)
    (h03 : angle_bisector_line P28 P09 P17 P29 L12)
    (h04 : between P18 P07 P28)
    : angle_bisector P29 P18 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0284
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0284

theorem v06_sealed_holdout_0285
    (P02 P03 P09 P11 P13 P16 P19 P20 P22 P23 P25 P27 P28 : Point)
    (L10 L26 : Line)
    (C12 : Circle)
    (h00 : angle_bisector_line P25 P19 P23 P03 L10)
    (h01 : midpoint P13 P28 P11)
    (h02 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    (h03 : line_circle_intersection P19 L26 C12)
    (h04 : between P22 P03 P16)
    : angle_bisector P25 P19 P23 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0285
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0285

theorem v06_sealed_holdout_0286
    (P02 P03 P04 P07 P09 P14 P15 P16 P19 P20 P23 P24 P26 P27 P31 : Point)
    (L12 : Line)
    (C02 C06 : Circle)
    (h00 : directed_angle_eq_mod_pi P02 P26 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : angle_bisector_line P20 P07 P16 P27 L12)
    (h03 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    (h04 : circle_circle_intersection P19 C06 C02)
    : directed_angle_eq_mod_pi P02 P26 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0286
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0286

theorem v06_sealed_holdout_0287
    (P00 P02 P04 P06 P07 P09 P16 P18 P19 P21 P23 P25 P29 P30 : Point)
    (C02 C22 : Circle)
    (h00 : directed_angle_eq_mod_2pi P23 P29 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : midpoint P00 P09 P18)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : between P04 P21 P06)
    : directed_angle_eq_mod_2pi P23 P29 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0287
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0287

theorem v06_sealed_holdout_0288
    (P03 P04 P05 P07 P11 P15 P16 P17 P23 P24 P26 P30 P31 : Point)
    (L18 : Line)
    (C10 : Circle)
    (h00 : directed_angle_eq_mod_pi P04 P26 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : between P05 P04 P03)
    (h03 : line_circle_intersection P03 L18 C10)
    (h04 : between P11 P30 P17)
    : directed_angle_eq_mod_pi P04 P26 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0288
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0288

theorem v06_sealed_holdout_0289
    (P02 P05 P07 P08 P09 P14 P15 P16 P18 P21 P25 P26 P27 P28 P29 P30 : Point)
    (h00 : directed_angle_eq_mod_2pi P25 P29 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P26 P02)
    (h02 : area_le P14 P27 P08 P21 P02 P15)
    (h03 : midpoint P15 P26 P05)
    (h04 : midpoint P18 P07 P28)
    : directed_angle_eq_mod_2pi P25 P29 P09 P16 P26 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0289
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0289

theorem v06_sealed_holdout_0290
    (P03 P07 P09 P11 P12 P14 P16 P19 P21 P22 P25 P27 P29 P30 : Point)
    (L18 L24 : Line)
    (C26 C29 : Circle)
    (h00 : circle_through_three_noncollinear_points P14 P09 P16 C29)
    (h01 : line_circle_intersection P03 L18 C26)
    (h02 : midpoint P19 P22 P25)
    (h03 : angle_bisector_line P29 P11 P16 P27 L24)
    (h04 : area_le P25 P16 P07 P30 P21 P12)
    : triangle_pred P14 P09 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0290
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0290

theorem v06_sealed_holdout_0291
    (P00 P03 P04 P05 P08 P09 P10 P11 P12 P13 P14 P18 P19 P23 P25 P26 P27 P29 P30 P31 : Point)
    (h00 : equilateral P03 P08 P05)
    (h01 : area_le P23 P18 P13 P08 P03 P30)
    (h02 : area_le P26 P31 P04 P09 P14 P19)
    (h03 : directed_angle_eq_mod_pi P29 P12 P27 P10 P25 P08)
    (h04 : area_le P00 P25 P18 P11 P04 P29)
    : triangle_pred P03 P08 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0291
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0291

theorem v06_sealed_holdout_0292
    (P02 P04 P06 P07 P09 P14 P15 P16 P17 P18 P19 P21 P24 P27 P29 P30 : Point)
    (L10 : Line)
    (C00 C11 : Circle)
    (h00 : circle_through_three_noncollinear_points P16 P09 P17 C11)
    (h01 : area_le P30 P27 P24 P21 P18 P15)
    (h02 : line_circle_intersection P19 L10 C00)
    (h03 : midpoint P04 P21 P06)
    (h04 : area_le P07 P02 P29 P24 P19 P14)
    : triangle_pred P16 P09 P17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0292
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0292

theorem v06_sealed_holdout_0293
    (P03 P04 P05 P06 P07 P08 P11 P16 P17 P27 P28 P30 : Point)
    (L00 L02 : Line)
    (C14 : Circle)
    (h00 : equilateral P05 P08 P06)
    (h01 : midpoint P05 P04 P03)
    (h02 : angle_bisector_line P27 P07 P16 P28 L00)
    (h03 : midpoint P11 P30 P17)
    (h04 : line_circle_intersection P03 L02 C14)
    : triangle_pred P05 P08 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0293
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0293

theorem v06_sealed_holdout_0294
    (P05 P06 P07 P08 P12 P13 P14 P15 P16 P17 P18 P19 P20 P21 P26 P28 : Point)
    (h00 : equilateral P06 P08 P05)
    (h01 : area_le P12 P13 P14 P15 P16 P17)
    (h02 : between P15 P26 P05)
    (h03 : between P18 P07 P28)
    (h04 : area_le P21 P20 P19 P18 P17 P16)
    : triangle_pred P06 P08 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0294
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0294

theorem v06_sealed_holdout_0295
    (P00 P01 P02 P03 P07 P10 P16 P17 P19 P22 P24 P25 P28 P29 P30 P31 : Point)
    (L02 : Line)
    (C30 : Circle)
    (RF62 : Reflection)
    (h00 : between P24 P17 P10)
    (h01 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    (h02 : line_circle_intersection P03 L02 C30)
    (h03 : midpoint P25 P16 P07)
    (h04 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    : reflection_image RF62 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0295
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0295

theorem v06_sealed_holdout_0296
    (P03 P04 P06 P08 P09 P10 P11 P12 P15 P16 P18 P21 P25 P26 P27 P29 P31 : Point)
    (L00 L08 : Line)
    (HOM47 : Homothety)
    (h00 : area_le P31 P26 P21 P16 P11 P06)
    (h01 : angle_bisector_line P25 P04 P15 P27 L08)
    (h02 : area_le P29 P12 P27 P10 P25 P08)
    (h03 : angle_bisector_line P03 P11 P16 P27 L00)
    (h04 : directed_angle_eq_mod_pi P03 P06 P09 P12 P15 P18)
    : homothety_image HOM47 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0296
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0296

theorem v06_sealed_holdout_0297
    (P00 P03 P04 P06 P11 P15 P16 P23 P26 P27 P29 : Point)
    (L12 L20 : Line)
    (C10 C18 C19 : Circle)
    (INV36 : Inversion)
    (h00 : directed_angle_eq_mod_pi P06 P03 P00 P29 P26 P23)
    (h01 : angle_bisector_line P26 P04 P15 P27 L20)
    (h02 : circle_circle_intersection P03 C18 C19)
    (h03 : angle_bisector_line P04 P11 P16 P27 L12)
    (h04 : circle_circle_intersection P03 C10 C18)
    : inversion_image INV36 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0297
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0297

theorem v06_sealed_holdout_0298
    (P03 P04 P06 P10 P11 P13 P17 P19 P20 P23 P24 P30 P31 : Point)
    (L18 L24 : Line)
    (C06 C10 C18 C26 : Circle)
    (SP29 : SpiralSimilarity)
    (h00 : line_circle_intersection P19 L24 C06)
    (h01 : line_circle_intersection P03 L18 C10)
    (h02 : area_le P11 P30 P17 P04 P23 P10)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : area_le P17 P24 P31 P06 P13 P20)
    : spiral_similarity_center SP29 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0298
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0298

theorem v06_sealed_holdout_0299
    (P00 P03 P08 P09 P19 P27 P31 : Point)
    (L18 : Line)
    (C10 C14 C15 : Circle)
    (h00 : P31 = P09)
    (h01 : P08 = P19)
    (h02 : P27 = P00)
    (h03 : circle_circle_intersection P31 C14 C15)
    (h04 : line_circle_intersection P03 L18 C10)
    : rotation_preserves_collinear P31 P08 P27 P09 P19 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0299
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0299

theorem v06_sealed_holdout_0300
    (P00 P01 P03 P08 P16 P19 P22 P27 P28 P29 P30 P31 : Point)
    (L10 : Line)
    (C02 C03 C14 C16 : Circle)
    (h00 : circle_with_center_through_point P08 P27 C03)
    (h01 : midpoint P22 P03 P16)
    (h02 : line_circle_intersection P19 L10 C16)
    (h03 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    (h04 : circle_circle_intersection P19 C14 C02)
    : on_circle P27 C03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0300
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0300

theorem v06_sealed_holdout_0301
    (P00 P03 P04 P08 P10 P11 P12 P16 P18 P25 P27 P29 P30 P31 : Point)
    (L02 L28 : Line)
    (C11 C30 : Circle)
    (h00 : circle_through_three_noncollinear_points P29 P30 P31 C11)
    (h01 : area_le P29 P12 P27 P10 P25 P08)
    (h02 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    (h03 : angle_bisector_line P08 P11 P16 P27 L28)
    (h04 : line_circle_intersection P03 L02 C30)
    : on_circle P29 C11 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0301
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0301

theorem v06_sealed_holdout_0302
    (P02 P03 P04 P06 P07 P08 P11 P13 P21 P23 P25 P28 P29 : Point)
    (L02 L21 : Line)
    (C07 C22 : Circle)
    (h00 : line_circle_intersection P02 L21 C07)
    (h01 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    (h02 : between P07 P02 P29)
    (h03 : line_circle_intersection P03 L02 C22)
    (h04 : midpoint P13 P28 P11)
    : on_circle P02 C07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0302
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0302

theorem v06_sealed_holdout_0303
    (P03 P04 P05 P10 P11 P16 P17 P20 P22 P23 P27 P30 P31 : Point)
    (L20 : Line)
    (C04 C18 C26 : Circle)
    (h00 : chord P31 P27 C04)
    (h01 : area_le P11 P30 P17 P04 P23 P10)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : angle_bisector_line P10 P11 P16 P27 L20)
    (h04 : between P20 P05 P22)
    : on_circle P31 C04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0303
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0303

theorem v06_sealed_holdout_0304
    (P01 P05 P07 P10 P14 P15 P16 P17 P18 P19 P20 P21 P24 P26 P27 P28 P30 : Point)
    (L09 : Line)
    (C04 : Circle)
    (h00 : line_circle_intersection P21 L09 C04)
    (h01 : area_le P21 P20 P19 P18 P17 P16)
    (h02 : area_le P24 P01 P10 P19 P28 P05)
    (h03 : area_le P27 P14 P01 P20 P07 P26)
    (h04 : area_le P30 P27 P24 P21 P18 P15)
    : on_line P21 L09 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0304
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0304

theorem v06_sealed_holdout_0305
    (P00 P01 P02 P11 P12 P17 P19 P22 P23 P28 P29 P30 P31 : Point)
    (L07 L10 L26 : Line)
    (C04 C16 C20 : Circle)
    (h00 : line_circle_intersection P17 L07 C04)
    (h01 : line_circle_intersection P19 L10 C16)
    (h02 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    (h03 : line_circle_intersection P19 L26 C20)
    (h04 : area_le P02 P23 P12 P01 P22 P11)
    : on_line P17 L07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0305
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0305

theorem v06_sealed_holdout_0306
    (P03 P05 P06 P08 P09 P11 P12 P15 P16 P19 P23 P27 : Point)
    (L00 L02 L07 L10 L28 : Line)
    (C16 C30 : Circle)
    (h00 : altitude P06 P12 P11 P23 L07)
    (h01 : angle_bisector_line P03 P05 P15 P27 L00)
    (h02 : angle_bisector_line P08 P09 P16 P27 L28)
    (h03 : line_circle_intersection P03 L02 C30)
    (h04 : line_circle_intersection P19 L10 C16)
    : on_line P11 L07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0306
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0306

theorem v06_sealed_holdout_0307
    (P10 P14 P15 P16 P17 P19 P20 P27 P29 : Point)
    (L00 L10 L20 : Line)
    (C02 C08 C14 : Circle)
    (h00 : angle_bisector_line P27 P16 P17 P29 L20)
    (h01 : circle_circle_intersection P19 C14 C02)
    (h02 : between P10 P15 P20)
    (h03 : line_circle_intersection P19 L10 C08)
    (h04 : angle_bisector_line P19 P14 P16 P27 L00)
    : on_line P27 L20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0307
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0307

theorem v06_sealed_holdout_0308
    (P05 P06 P07 P09 P13 P15 P17 P19 P20 P22 P24 P27 P31 : Point)
    (L20 L24 L26 : Line)
    (C04 C28 : Circle)
    (h00 : line_circle_intersection P20 L20 C28)
    (h01 : angle_bisector_line P05 P06 P15 P27 L24)
    (h02 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    (h03 : area_le P20 P05 P22 P07 P24 P09)
    (h04 : line_circle_intersection P19 L26 C04)
    : on_line P20 L20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0308
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0308

theorem v06_sealed_holdout_0309
    (P01 P05 P08 P11 P16 P19 P24 P27 P30 P31 : Point)
    (L00 L10 : Line)
    (C02 C24 C30 : Circle)
    (h00 : equilateral P01 P05 P31)
    (h01 : line_circle_intersection P19 L10 C24)
    (h02 : angle_bisector_line P11 P08 P16 P27 L00)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : between P30 P27 P24)
    : equal_length P01 P05 P05 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0309
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0309

theorem v06_sealed_holdout_0310
    (P01 P02 P03 P04 P05 P06 P09 P12 P15 P16 P19 P20 P23 P24 P29 : Point)
    (L26 : Line)
    (C20 : Circle)
    (h00 : length_sum P06 P23 P29 P09 P16 P24)
    (h01 : area_le P01 P24 P15 P06 P29 P20)
    (h02 : line_circle_intersection P19 L26 C20)
    (h03 : midpoint P02 P23 P12)
    (h04 : between P05 P04 P03)
    : length_sum P29 P09 P06 P23 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0310
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0310

theorem v06_sealed_holdout_0311
    (P01 P02 P03 P05 P08 P12 P13 P14 P15 P16 P19 P26 P27 : Point)
    (C02 C22 : Circle)
    (h00 : equal_length P03 P02 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : directed_angle_eq_mod_pi P08 P01 P26 P19 P12 P05)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : midpoint P12 P13 P14)
    : equal_length P03 P02 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0311
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0311

theorem v06_sealed_holdout_0312
    (P01 P02 P05 P09 P12 P13 P16 P19 P20 P21 P22 P23 P24 P25 P27 P28 P31 : Point)
    (L10 : Line)
    (C20 : Circle)
    (h00 : area_eq P24 P05 P21 P01 P12 P23)
    (h01 : area_eq P01 P12 P23 P02 P13 P25)
    (h02 : line_circle_intersection P27 L10 C20)
    (h03 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    (h04 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    : area_eq P24 P05 P21 P02 P13 P25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0312
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0312

theorem v06_sealed_holdout_0313
    (P02 P04 P05 P06 P07 P13 P15 P16 P18 P23 P26 P27 P31 : Point)
    (C22 C30 : Circle)
    (h00 : equal_length P05 P02 P15 P27)
    (h01 : equal_length P15 P27 P06 P16)
    (h02 : circle_circle_intersection P07 C30 C22)
    (h03 : between P23 P18 P13)
    (h04 : between P26 P31 P04)
    : equal_length P05 P02 P06 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0313
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0313

theorem v06_sealed_holdout_0314
    (P01 P03 P04 P06 P08 P15 P16 P17 P19 P21 P22 P23 P24 P25 P27 P29 : Point)
    (L14 L28 : Line)
    (C18 C26 : Circle)
    (h00 : angle_bisector_line P27 P19 P24 P03 L14)
    (h01 : angle_bisector_line P16 P04 P17 P27 L28)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : area_le P01 P08 P15 P22 P29 P04)
    (h04 : area_le P04 P21 P06 P23 P08 P25)
    : angle_bisector P27 P19 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0314
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0314

theorem v06_sealed_holdout_0315
    (P00 P01 P02 P03 P04 P05 P12 P19 P20 P23 P24 : Point)
    (L12 L18 L26 : Line)
    (C10 C20 : Circle)
    (h00 : angle_bisector_line P23 P20 P24 P03 L12)
    (h01 : line_circle_intersection P19 L26 C20)
    (h02 : midpoint P02 P23 P12)
    (h03 : area_le P05 P04 P03 P02 P01 P00)
    (h04 : line_circle_intersection P03 L18 C10)
    : angle_bisector P23 P20 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0315
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0315

theorem v06_sealed_holdout_0316
    (P00 P03 P07 P15 P16 P19 P23 P24 P27 P31 : Point)
    (L18 : Line)
    (C02 C14 C22 : Circle)
    (h00 : directed_angle_eq_mod_pi P00 P27 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : line_circle_intersection P03 L18 C02)
    (h04 : circle_circle_intersection P19 C14 C02)
    : directed_angle_eq_mod_pi P00 P27 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0316
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0316

theorem v06_sealed_holdout_0317
    (P01 P02 P03 P06 P07 P09 P11 P16 P18 P19 P21 P22 P23 P25 P28 P30 P31 : Point)
    (L02 : Line)
    (C30 : Circle)
    (h00 : directed_angle_eq_mod_2pi P21 P30 P09 P22 P31 P07)
    (h01 : directed_angle_eq_mod_2pi P22 P31 P07 P16 P25 P02)
    (h02 : area_le P18 P23 P28 P01 P06 P11)
    (h03 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    (h04 : line_circle_intersection P03 L02 C30)
    : directed_angle_eq_mod_2pi P21 P30 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0317
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0317

theorem v06_sealed_holdout_0318
    (P02 P03 P07 P08 P10 P12 P13 P15 P16 P18 P23 P24 P25 P27 P29 P30 P31 : Point)
    (C10 C18 : Circle)
    (h00 : directed_angle_eq_mod_pi P02 P27 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : area_le P23 P18 P13 P08 P03 P30)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : directed_angle_eq_mod_pi P29 P12 P27 P10 P25 P08)
    : directed_angle_eq_mod_pi P02 P27 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0318
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0318

theorem v06_sealed_holdout_0319
    (P01 P02 P04 P06 P07 P08 P09 P15 P16 P21 P23 P25 P30 P31 : Point)
    (L19 : Line)
    (C11 : Circle)
    (h00 : directed_angle_eq_mod_2pi P23 P30 P09 P21 P31 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P31 P07 P16 P25 P02)
    (h02 : line_circle_intersection P15 L19 C11)
    (h03 : midpoint P01 P08 P15)
    (h04 : area_le P04 P21 P06 P23 P08 P25)
    : directed_angle_eq_mod_2pi P23 P30 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0319
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0319

theorem v06_sealed_holdout_0320
    (P04 P05 P09 P10 P11 P12 P15 P16 P17 P19 P23 P27 P28 P30 : Point)
    (L00 L08 L10 : Line)
    (C15 C24 : Circle)
    (h00 : circle_through_three_noncollinear_points P12 P09 P16 C15)
    (h01 : angle_bisector_line P17 P05 P15 P27 L08)
    (h02 : line_circle_intersection P19 L10 C24)
    (h03 : angle_bisector_line P27 P11 P16 P28 L00)
    (h04 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    : triangle_pred P12 P09 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0320
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0320

theorem v06_sealed_holdout_0321
    (P00 P01 P05 P06 P07 P09 P12 P13 P14 P17 P18 P19 P23 P27 P28 : Point)
    (L26 : Line)
    (C20 : Circle)
    (h00 : equilateral P01 P09 P05)
    (h01 : area_le P09 P00 P23 P14 P05 P28)
    (h02 : midpoint P12 P13 P14)
    (h03 : line_circle_intersection P19 L26 C20)
    (h04 : area_le P18 P07 P28 P17 P06 P27)
    : triangle_pred P01 P09 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0321
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0321

theorem v06_sealed_holdout_0322
    (P02 P03 P09 P10 P13 P14 P16 P19 P20 P22 P25 P27 P28 P31 : Point)
    (C02 C22 C29 : Circle)
    (h00 : circle_through_three_noncollinear_points P14 P10 P16 C29)
    (h01 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    (h02 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    (h03 : midpoint P22 P03 P16)
    (h04 : circle_circle_intersection P19 C22 C02)
    : triangle_pred P14 P10 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0322
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0322

theorem v06_sealed_holdout_0323
    (P00 P03 P04 P05 P08 P09 P10 P11 P12 P14 P18 P19 P25 P26 P27 P29 P31 : Point)
    (C02 C14 : Circle)
    (h00 : equilateral P03 P09 P05)
    (h01 : circle_circle_intersection P19 C14 C02)
    (h02 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    (h03 : area_le P29 P12 P27 P10 P25 P08)
    (h04 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    : triangle_pred P03 P09 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0323
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0323

theorem v06_sealed_holdout_0324
    (P01 P04 P05 P08 P09 P12 P15 P16 P19 P22 P24 P27 P29 P30 P31 : Point)
    (L16 : Line)
    (C02 C14 : Circle)
    (h00 : equilateral P04 P09 P05)
    (h01 : between P30 P27 P24)
    (h02 : directed_angle_eq_mod_pi P01 P08 P15 P22 P29 P04)
    (h03 : angle_bisector_line P31 P12 P16 P27 L16)
    (h04 : circle_circle_intersection P19 C14 C02)
    : triangle_pred P04 P09 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0324
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0324

theorem v06_sealed_holdout_0325
    (P00 P01 P02 P03 P04 P05 P08 P09 P10 P11 P14 P19 P20 P30 P31 : Point)
    (L26 : Line)
    (C02 C18 C28 : Circle)
    (RF16 : Reflection)
    (h00 : directed_angle_eq_mod_pi P10 P31 P20 P09 P30 P19)
    (h01 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : line_circle_intersection P19 L26 C28)
    (h04 : between P14 P11 P08)
    : reflection_image RF16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0325
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0325

theorem v06_sealed_holdout_0326
    (P03 P05 P06 P07 P12 P13 P14 P15 P16 P18 P19 P20 P21 P26 P27 P28 : Point)
    (L28 : Line)
    (C02 : Circle)
    (HOM61 : Homothety)
    (h00 : line_circle_intersection P03 L28 C02)
    (h01 : midpoint P12 P13 P14)
    (h02 : area_le P15 P26 P05 P16 P27 P06)
    (h03 : between P18 P07 P28)
    (h04 : between P21 P20 P19)
    : homothety_image HOM61 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0326
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0326

theorem v06_sealed_holdout_0327
    (P02 P03 P07 P15 P16 P19 P22 P25 P28 P31 : Point)
    (C14 C18 C19 C30 : Circle)
    (INV46 : Inversion)
    (h00 : circle_circle_intersection P15 C14 C30)
    (h01 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    (h02 : between P22 P03 P16)
    (h03 : midpoint P25 P16 P07)
    (h04 : circle_circle_intersection P03 C18 C19)
    : inversion_image INV46 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0327
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0327

theorem v06_sealed_holdout_0328
    (P03 P06 P09 P13 P15 P19 P20 P31 : Point)
    (L02 L10 L18 L20 : Line)
    (C08 C22 C26 : Circle)
    (SP35 : SpiralSimilarity)
    (h00 : angle_bisector_line P20 P15 P31 P13 L20)
    (h01 : line_circle_intersection P03 L02 C22)
    (h02 : line_circle_intersection P19 L10 C08)
    (h03 : line_circle_intersection P03 L18 C26)
    (h04 : between P03 P06 P09)
    : spiral_similarity_center SP35 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0328
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0328

theorem v06_sealed_holdout_0329
    (P00 P03 P06 P08 P09 P10 P15 P19 P20 P25 P27 P29 P30 P31 : Point)
    (h00 : P29 = P08)
    (h01 : P09 = P19)
    (h02 : P27 = P31)
    (h03 : midpoint P06 P03 P00)
    (h04 : area_le P10 P15 P20 P25 P30 P03)
    : rotation_preserves_collinear P29 P09 P27 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0329
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0329

theorem v06_sealed_holdout_0330
    (P02 P03 P05 P06 P08 P11 P12 P14 P17 P19 P21 P24 P26 P28 P31 : Point)
    (C02 C07 C30 : Circle)
    (h00 : circle_with_center_through_point P06 P28 C07)
    (h01 : area_le P08 P17 P26 P03 P12 P21)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : directed_angle_eq_mod_pi P14 P11 P08 P05 P02 P31)
    (h04 : midpoint P17 P24 P31)
    : on_circle P28 C07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0330
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0330

theorem v06_sealed_holdout_0331
    (P01 P03 P05 P09 P15 P16 P19 P26 P27 P30 P31 : Point)
    (L08 L10 L18 : Line)
    (C10 C13 C24 : Circle)
    (h00 : circle_through_three_noncollinear_points P27 P31 P30 C13)
    (h01 : midpoint P15 P26 P05)
    (h02 : angle_bisector_line P01 P09 P16 P27 L08)
    (h03 : line_circle_intersection P19 L10 C24)
    (h04 : line_circle_intersection P03 L18 C10)
    : on_circle P27 C13 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0331
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0331

theorem v06_sealed_holdout_0332
    (P00 P03 P07 P10 P16 P21 P22 P25 P31 : Point)
    (L18 L21 : Line)
    (C02 C21 : Circle)
    (h00 : line_circle_intersection P00 L21 C21)
    (h01 : midpoint P22 P03 P16)
    (h02 : between P25 P16 P07)
    (h03 : line_circle_intersection P03 L18 C02)
    (h04 : midpoint P31 P10 P21)
    : on_circle P00 C21 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0332
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0332

theorem v06_sealed_holdout_0333
    (P00 P03 P06 P08 P09 P10 P12 P13 P15 P16 P18 P25 P27 P28 P29 : Point)
    (L24 : Line)
    (C12 : Circle)
    (h00 : chord P29 P28 C12)
    (h01 : directed_angle_eq_mod_pi P29 P12 P27 P10 P25 P08)
    (h02 : midpoint P00 P25 P18)
    (h03 : between P03 P06 P09)
    (h04 : angle_bisector_line P13 P15 P16 P27 L24)
    : on_circle P29 C12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0333
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0333

theorem v06_sealed_holdout_0334
    (P02 P03 P07 P09 P13 P16 P19 P20 P27 P29 : Point)
    (L02 L10 L11 : Line)
    (C08 C20 C22 : Circle)
    (h00 : line_circle_intersection P19 L11 C20)
    (h01 : between P07 P02 P29)
    (h02 : line_circle_intersection P03 L02 C22)
    (h03 : line_circle_intersection P19 L10 C08)
    (h04 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    : on_line P19 L11 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0334
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0334

theorem v06_sealed_holdout_0335
    (P00 P05 P06 P07 P09 P15 P16 P19 P20 P22 P24 P27 : Point)
    (L09 L24 L28 : Line)
    (C02 C20 C22 : Circle)
    (h00 : line_circle_intersection P15 L09 C20)
    (h01 : angle_bisector_line P00 P06 P15 P27 L28)
    (h02 : angle_bisector_line P05 P09 P16 P27 L24)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : area_le P20 P05 P22 P07 P24 P09)
    : on_line P15 L09 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0335
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0335

theorem v06_sealed_holdout_0336
    (P01 P03 P04 P11 P12 P13 P14 P16 P19 P23 P27 : Point)
    (L00 L10 L13 : Line)
    (C10 C18 C24 : Circle)
    (h00 : altitude P04 P13 P11 P23 L13)
    (h01 : circle_circle_intersection P03 C10 C18)
    (h02 : line_circle_intersection P19 L10 C24)
    (h03 : angle_bisector_line P11 P12 P16 P27 L00)
    (h04 : midpoint P27 P14 P01)
    : on_line P11 L13 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0336
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0336

theorem v06_sealed_holdout_0337
    (P00 P01 P03 P07 P10 P11 P12 P16 P17 P18 P21 P22 P25 P28 P29 P30 P31 : Point)
    (L24 : Line)
    (C10 C18 : Circle)
    (h00 : angle_bisector_line P25 P17 P18 P29 L24)
    (h01 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h02 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    (h03 : area_le P31 P10 P21 P00 P11 P22)
    (h04 : circle_circle_intersection P03 C10 C18)
    : on_line P25 L24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0337
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0337

theorem v06_sealed_holdout_0338
    (P00 P05 P06 P07 P08 P09 P13 P14 P16 P18 P19 P23 P25 P26 P27 P28 : Point)
    (L22 L28 : Line)
    (C12 : Circle)
    (h00 : line_circle_intersection P18 L22 C12)
    (h01 : midpoint P00 P25 P18)
    (h02 : angle_bisector_line P08 P09 P16 P27 L28)
    (h03 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    (h04 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    : on_line P18 L22 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0338
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0338

theorem v06_sealed_holdout_0339
    (P00 P02 P03 P06 P07 P09 P10 P11 P13 P14 P15 P16 P19 P20 P24 P25 P26 P28 P29 P30 P31 : Point)
    (h00 : equilateral P31 P06 P00)
    (h01 : directed_angle_eq_mod_pi P07 P02 P29 P24 P19 P14)
    (h02 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    (h03 : directed_angle_eq_mod_pi P13 P28 P11 P26 P09 P24)
    (h04 : midpoint P16 P09 P02)
    : equal_length P31 P06 P06 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0339
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0339

theorem v06_sealed_holdout_0340
    (P04 P05 P07 P09 P10 P11 P13 P16 P18 P20 P22 P23 P24 P27 P29 : Point)
    (L14 L20 : Line)
    (C16 : Circle)
    (h00 : length_sum P04 P24 P29 P09 P16 P23)
    (h01 : line_circle_intersection P11 L14 C16)
    (h02 : angle_bisector_line P10 P09 P16 P27 L20)
    (h03 : directed_angle_eq_mod_pi P20 P05 P22 P07 P24 P09)
    (h04 : midpoint P23 P18 P13)
    : length_sum P29 P09 P04 P24 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0340
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0340

theorem v06_sealed_holdout_0341
    (P01 P03 P05 P15 P16 P18 P19 P21 P23 P24 P27 P30 : Point)
    (C02 C06 C30 : Circle)
    (h00 : equal_length P01 P03 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : circle_circle_intersection P23 C30 C06)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    : equal_length P01 P03 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0341
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0341

theorem v06_sealed_holdout_0342
    (P01 P02 P06 P12 P13 P16 P19 P21 P22 P23 P24 P31 : Point)
    (L04 : Line)
    (C02 C06 : Circle)
    (h00 : area_eq P22 P06 P21 P01 P12 P23)
    (h01 : area_eq P01 P12 P23 P02 P13 P24)
    (h02 : angle_bisector_line P02 P16 P31 P13 L04)
    (h03 : between P02 P23 P12)
    (h04 : circle_circle_intersection P19 C06 C02)
    : area_eq P22 P06 P21 P02 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0342
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0342

theorem v06_sealed_holdout_0343
    (P00 P01 P03 P04 P05 P08 P09 P12 P13 P14 P15 P16 P23 P26 P27 : Point)
    (h00 : equal_length P03 P04 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : midpoint P08 P01 P26)
    (h03 : between P09 P00 P23)
    (h04 : midpoint P12 P13 P14)
    : equal_length P03 P04 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0343
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0343

theorem v06_sealed_holdout_0344
    (P02 P03 P09 P10 P15 P16 P19 P20 P22 P25 P26 P28 P30 P31 : Point)
    (L06 L10 : Line)
    (C08 C26 : Circle)
    (h00 : tangent_chord_angle P16 P03 P26 L06 C26)
    (h01 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    (h02 : line_circle_intersection P19 L10 C08)
    (h03 : midpoint P16 P09 P02)
    (h04 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    : on_circle P26 C26 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0344
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0344

theorem v06_sealed_holdout_0345
    (P03 P04 P05 P07 P09 P13 P17 P18 P20 P21 P22 P23 P24 P26 P31 : Point)
    (L14 : Line)
    (h00 : angle_bisector_line P21 P22 P23 P03 L14)
    (h01 : midpoint P17 P24 P31)
    (h02 : directed_angle_eq_mod_pi P20 P05 P22 P07 P24 P09)
    (h03 : between P23 P18 P13)
    (h04 : between P26 P31 P04)
    : angle_bisector P21 P22 P23 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0345
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0345

theorem v06_sealed_holdout_0346
    (P01 P03 P07 P08 P14 P15 P16 P18 P20 P21 P23 P24 P26 P27 P28 P30 P31 : Point)
    (h00 : directed_angle_eq_mod_pi P30 P28 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    (h03 : area_le P30 P27 P24 P21 P18 P15)
    (h04 : between P01 P08 P15)
    : directed_angle_eq_mod_pi P30 P28 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0346
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0346

theorem v06_sealed_holdout_0347
    (P02 P03 P04 P05 P07 P08 P09 P12 P16 P17 P19 P21 P25 P26 P30 P31 : Point)
    (L23 : Line)
    (C07 : Circle)
    (h00 : directed_angle_eq_mod_2pi P19 P31 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : line_circle_intersection P31 L23 C07)
    (h03 : between P05 P04 P03)
    (h04 : area_le P08 P17 P26 P03 P12 P21)
    : directed_angle_eq_mod_2pi P19 P31 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0347
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0347

theorem v06_sealed_holdout_0348
    (P00 P03 P05 P07 P09 P14 P15 P16 P19 P23 P24 P28 P31 : Point)
    (C02 C14 C18 C19 : Circle)
    (h00 : directed_angle_eq_mod_pi P00 P28 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h03 : circle_circle_intersection P03 C18 C19)
    (h04 : circle_circle_intersection P19 C14 C02)
    : directed_angle_eq_mod_pi P00 P28 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0348
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0348

theorem v06_sealed_holdout_0349
    (P02 P03 P07 P09 P13 P16 P19 P21 P22 P25 P30 P31 : Point)
    (L28 : Line)
    (C02 C30 : Circle)
    (h00 : directed_angle_eq_mod_2pi P21 P31 P09 P22 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P22 P30 P07 P16 P25 P02)
    (h02 : angle_bisector_line P09 P16 P31 P13 L28)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : midpoint P22 P03 P16)
    : directed_angle_eq_mod_2pi P21 P31 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0349
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0349

theorem v06_sealed_holdout_0350
    (P03 P05 P08 P10 P11 P12 P13 P16 P18 P20 P22 P23 P25 P27 P29 : Point)
    (L02 : Line)
    (C01 C22 : Circle)
    (h00 : circle_through_three_noncollinear_points P10 P11 P16 C01)
    (h01 : midpoint P20 P05 P22)
    (h02 : midpoint P23 P18 P13)
    (h03 : line_circle_intersection P03 L02 C22)
    (h04 : area_le P29 P12 P27 P10 P25 P08)
    : triangle_pred P10 P11 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0350
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0350

theorem v06_sealed_holdout_0351
    (P01 P04 P05 P06 P07 P08 P10 P12 P14 P16 P20 P21 P23 P24 P25 P26 P27 P30 P31 : Point)
    (L20 : Line)
    (h00 : equilateral P31 P10 P05)
    (h01 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    (h02 : between P30 P27 P24)
    (h03 : angle_bisector_line P26 P12 P16 P27 L20)
    (h04 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    : triangle_pred P31 P10 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0351
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0351

theorem v06_sealed_holdout_0352
    (P00 P03 P04 P05 P08 P10 P12 P16 P17 P21 P26 P27 : Point)
    (L02 L28 : Line)
    (C06 C15 : Circle)
    (h00 : circle_through_three_noncollinear_points P12 P10 P16 C15)
    (h01 : line_circle_intersection P03 L02 C06)
    (h02 : midpoint P05 P04 P03)
    (h03 : area_le P08 P17 P26 P03 P12 P21)
    (h04 : angle_bisector_line P00 P16 P17 P27 L28)
    : triangle_pred P12 P10 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0352
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0352

theorem v06_sealed_holdout_0353
    (P01 P05 P06 P07 P10 P12 P13 P14 P15 P16 P17 P18 P19 P27 P28 : Point)
    (L20 : Line)
    (C02 C14 : Circle)
    (h00 : equilateral P01 P10 P05)
    (h01 : angle_bisector_line P18 P06 P15 P27 L20)
    (h02 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h03 : circle_circle_intersection P19 C14 C02)
    (h04 : midpoint P18 P07 P28)
    : triangle_pred P01 P10 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0353
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0353

theorem v06_sealed_holdout_0354
    (P02 P03 P05 P09 P10 P13 P16 P19 P20 P22 P23 P27 P29 : Point)
    (L10 : Line)
    (C02 C16 C30 : Circle)
    (h00 : equilateral P02 P10 P05)
    (h01 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    (h04 : line_circle_intersection P19 L10 C16)
    : triangle_pred P02 P10 P05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0354
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0354

theorem v06_sealed_holdout_0355
    (P03 P04 P08 P10 P12 P13 P16 P17 P18 P23 P25 P26 P27 P29 P30 P31 : Point)
    (L00 : Line)
    (C14 C15 : Circle)
    (RF34 : Reflection)
    (h00 : circle_circle_intersection P31 C14 C15)
    (h01 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    (h02 : between P26 P31 P04)
    (h03 : directed_angle_eq_mod_pi P29 P12 P27 P10 P25 P08)
    (h04 : angle_bisector_line P03 P16 P17 P27 L00)
    : reflection_image RF34 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0355
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0355

theorem v06_sealed_holdout_0356
    (P01 P02 P03 P04 P06 P07 P08 P13 P15 P16 P17 P21 P22 P29 P31 : Point)
    (L02 L20 : Line)
    (C14 : Circle)
    (HOM11 : Homothety)
    (h00 : angle_bisector_line P16 P17 P31 P13 L20)
    (h01 : line_circle_intersection P03 L02 C14)
    (h02 : area_le P01 P08 P15 P22 P29 P04)
    (h03 : midpoint P04 P21 P06)
    (h04 : between P07 P02 P29)
    : homothety_image HOM11 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0356
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0356

theorem v06_sealed_holdout_0357
    (P00 P01 P02 P03 P04 P05 P08 P10 P11 P12 P14 P17 P19 P20 P21 P26 P31 : Point)
    (C02 C30 : Circle)
    (INV56 : Inversion)
    (h00 : midpoint P10 P31 P20)
    (h01 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    (h02 : area_le P08 P17 P26 P03 P12 P21)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : between P14 P11 P08)
    : inversion_image INV56 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0357
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0357

theorem v06_sealed_holdout_0358
    (P05 P06 P07 P08 P12 P13 P14 P15 P16 P17 P18 P19 P20 P21 P26 P27 P28 P31 : Point)
    (SP41 : SpiralSimilarity)
    (h00 : between P17 P08 P31)
    (h01 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h02 : area_le P15 P26 P05 P16 P27 P06)
    (h03 : area_le P18 P07 P28 P17 P06 P27)
    (h04 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    : spiral_similarity_center SP41 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0358
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0358

theorem v06_sealed_holdout_0359
    (P03 P08 P10 P17 P19 P21 P24 P27 P28 P31 : Point)
    (L18 : Line)
    (C02 : Circle)
    (h00 : P27 = P08)
    (h01 : P10 = P19)
    (h02 : P28 = P31)
    (h03 : area_le P24 P17 P10 P03 P28 P21)
    (h04 : line_circle_intersection P03 L18 C02)
    : rotation_preserves_collinear P27 P10 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0359
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0359

theorem v06_sealed_holdout_0360
    (P00 P03 P04 P06 P09 P11 P12 P15 P18 P25 P27 P29 P31 : Point)
    (C07 C18 C26 : Circle)
    (h00 : circle_through_three_noncollinear_points P29 P31 P00 C07)
    (h01 : between P29 P12 P27)
    (h02 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    (h03 : area_le P03 P06 P09 P12 P15 P18)
    (h04 : circle_circle_intersection P03 C26 C18)
    : on_circle P29 C07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0360
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0360

theorem v06_sealed_holdout_0361
    (P00 P01 P03 P08 P10 P15 P16 P19 P20 P25 P27 P30 P31 : Point)
    (L16 L26 : Line)
    (C04 C15 : Circle)
    (h00 : circle_through_three_noncollinear_points P25 P00 P30 C15)
    (h01 : between P01 P08 P15)
    (h02 : angle_bisector_line P31 P10 P16 P27 L16)
    (h03 : line_circle_intersection P19 L26 C04)
    (h04 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    : on_circle P25 C15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0361
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0361

theorem v06_sealed_holdout_0362
    (P03 P08 P11 P12 P14 P17 P19 P21 P26 P30 : Point)
    (L21 : Line)
    (C02 C03 C22 C30 : Circle)
    (h00 : line_circle_intersection P30 L21 C03)
    (h01 : directed_angle_eq_mod_pi P08 P17 P26 P03 P12 P21)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : between P14 P11 P08)
    (h04 : circle_circle_intersection P19 C22 C02)
    : on_circle P30 C03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0362
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0362

theorem v06_sealed_holdout_0363
    (P01 P03 P10 P16 P17 P18 P19 P20 P21 P24 P27 P28 : Point)
    (L26 : Line)
    (C10 C18 C20 : Circle)
    (h00 : chord P27 P28 C20)
    (h01 : line_circle_intersection P19 L26 C20)
    (h02 : circle_circle_intersection P03 C10 C18)
    (h03 : area_le P21 P20 P19 P18 P17 P16)
    (h04 : between P24 P01 P10)
    : on_circle P27 C20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0363
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0363

theorem v06_sealed_holdout_0364
    (P00 P01 P03 P04 P05 P16 P19 P22 P26 P28 P29 P30 P31 : Point)
    (L14 : Line)
    (C02 C14 C18 C22 : Circle)
    (h00 : tangent_chord_angle P04 P05 P26 L14 C18)
    (h01 : between P22 P03 P16)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : area_le P28 P29 P30 P31 P00 P01)
    (h04 : circle_circle_intersection P19 C14 C02)
    : on_circle P26 C18 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0364
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0364

theorem v06_sealed_holdout_0365
    (P03 P06 P09 P10 P12 P13 P15 P16 P18 P27 P29 : Point)
    (L00 L02 L11 : Line)
    (C04 C30 : Circle)
    (h00 : line_circle_intersection P13 L11 C04)
    (h01 : between P29 P12 P27)
    (h02 : angle_bisector_line P03 P10 P16 P27 L00)
    (h03 : area_le P03 P06 P09 P12 P15 P18)
    (h04 : line_circle_intersection P03 L02 C30)
    : on_line P13 L11 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0365
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0365

theorem v06_sealed_holdout_0366
    (P02 P03 P04 P10 P11 P14 P15 P16 P19 P20 P23 P27 : Point)
    (L10 L12 L19 : Line)
    (C08 C18 C19 : Circle)
    (h00 : altitude P02 P14 P11 P23 L19)
    (h01 : circle_circle_intersection P03 C18 C19)
    (h02 : angle_bisector_line P04 P10 P16 P27 L12)
    (h03 : between P10 P15 P20)
    (h04 : line_circle_intersection P19 L10 C08)
    : on_line P11 L19 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0366
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0366

theorem v06_sealed_holdout_0367
    (P03 P04 P06 P10 P11 P13 P17 P18 P20 P23 P24 P29 P30 P31 : Point)
    (L28 : Line)
    (C18 C19 C26 : Circle)
    (h00 : angle_bisector_line P23 P18 P17 P29 L28)
    (h01 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    (h04 : circle_circle_intersection P03 C18 C19)
    : on_line P23 L28 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0367
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0367

theorem v06_sealed_holdout_0368
    (P03 P06 P07 P16 P17 P18 P19 P27 P28 : Point)
    (L10 L18 L24 L26 : Line)
    (C10 C24 C28 : Circle)
    (h00 : line_circle_intersection P16 L24 C28)
    (h01 : area_le P18 P07 P28 P17 P06 P27)
    (h02 : line_circle_intersection P19 L10 C24)
    (h03 : line_circle_intersection P03 L18 C10)
    (h04 : line_circle_intersection P19 L26 C28)
    : on_line P16 L24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0368
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0368

theorem v06_sealed_holdout_0369
    (P00 P03 P07 P12 P13 P16 P19 P27 P28 P29 P30 : Point)
    (L02 L10 L12 : Line)
    (C06 C16 : Circle)
    (h00 : equilateral P29 P07 P00)
    (h01 : line_circle_intersection P19 L10 C16)
    (h02 : midpoint P28 P29 P30)
    (h03 : angle_bisector_line P12 P13 P16 P27 L12)
    (h04 : line_circle_intersection P03 L02 C06)
    : equal_length P29 P07 P07 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0369
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0369

theorem v06_sealed_holdout_0370
    (P00 P02 P05 P06 P07 P09 P13 P14 P16 P17 P19 P23 P25 P26 P28 P29 P30 P31 : Point)
    (L04 : Line)
    (C02 C30 : Circle)
    (h00 : length_sum P02 P25 P29 P09 P16 P23)
    (h01 : angle_bisector_line P30 P17 P31 P13 L04)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : area_le P06 P19 P00 P13 P26 P07)
    (h04 : area_le P09 P00 P23 P14 P05 P28)
    : length_sum P29 P09 P02 P25 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0370
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0370

theorem v06_sealed_holdout_0371
    (P02 P04 P05 P09 P12 P14 P15 P16 P19 P27 P29 P31 : Point)
    (L10 : Line)
    (C08 : Circle)
    (h00 : equal_length P31 P04 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : midpoint P12 P29 P14)
    (h03 : line_circle_intersection P19 L10 C08)
    (h04 : between P16 P09 P02)
    : equal_length P31 P04 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0371
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0371

theorem v06_sealed_holdout_0372
    (P01 P02 P03 P06 P07 P12 P13 P18 P19 P20 P21 P23 P24 P25 : Point)
    (L18 : Line)
    (C18 : Circle)
    (h00 : area_eq P20 P07 P21 P01 P12 P23)
    (h01 : area_eq P01 P12 P23 P02 P13 P24)
    (h02 : between P19 P06 P25)
    (h03 : line_circle_intersection P03 L18 C18)
    (h04 : between P23 P18 P13)
    : area_eq P20 P07 P21 P02 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0372
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0372

theorem v06_sealed_holdout_0373
    (P01 P03 P04 P05 P14 P15 P16 P19 P24 P25 P26 P27 P30 : Point)
    (C02 C30 : Circle)
    (h00 : equal_length P01 P04 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : area_le P26 P15 P04 P25 P14 P03)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : between P30 P27 P24)
    : equal_length P01 P04 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0373
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0373

theorem v06_sealed_holdout_0374
    (P00 P01 P02 P03 P04 P05 P10 P12 P14 P21 P23 P26 P31 : Point)
    (L18 : Line)
    (C18 C19 C30 : Circle)
    (h00 : tangent_chord_angle P14 P04 P26 L18 C30)
    (h01 : circle_circle_intersection P03 C18 C19)
    (h02 : midpoint P31 P10 P21)
    (h03 : between P02 P23 P12)
    (h04 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    : on_circle P26 C30 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0374
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0374

theorem v06_sealed_holdout_0375
    (P00 P03 P06 P07 P09 P13 P16 P17 P19 P22 P23 P26 P27 : Point)
    (L10 L16 : Line)
    (C16 : Circle)
    (h00 : angle_bisector_line P19 P22 P23 P03 L16)
    (h01 : between P03 P06 P09)
    (h02 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    (h03 : line_circle_intersection P19 L10 C16)
    (h04 : angle_bisector_line P23 P16 P17 P27 L16)
    : angle_bisector P19 P22 P23 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0375
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0375

theorem v06_sealed_holdout_0376
    (P03 P07 P09 P11 P13 P15 P16 P19 P22 P23 P24 P25 P26 P28 P29 P31 : Point)
    (L18 : Line)
    (C26 : Circle)
    (h00 : directed_angle_eq_mod_pi P28 P29 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : area_le P13 P28 P11 P26 P09 P24)
    (h03 : line_circle_intersection P03 L18 C26)
    (h04 : between P19 P22 P25)
    : directed_angle_eq_mod_pi P28 P29 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0376
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0376

theorem v06_sealed_holdout_0377
    (P00 P02 P03 P05 P07 P09 P13 P16 P17 P19 P21 P25 P30 P31 : Point)
    (L02 L26 L28 : Line)
    (C04 C22 : Circle)
    (h00 : directed_angle_eq_mod_2pi P17 P00 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : angle_bisector_line P05 P17 P31 P13 L28)
    (h03 : line_circle_intersection P19 L26 C04)
    (h04 : line_circle_intersection P03 L02 C22)
    : directed_angle_eq_mod_2pi P17 P00 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0377
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0377

theorem v06_sealed_holdout_0378
    (P01 P03 P07 P14 P15 P16 P17 P20 P23 P24 P26 P27 P29 P30 P31 : Point)
    (L20 : Line)
    (h00 : directed_angle_eq_mod_pi P30 P29 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    (h03 : between P30 P27 P24)
    (h04 : angle_bisector_line P26 P16 P17 P27 L20)
    : directed_angle_eq_mod_pi P30 P29 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0378
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0378

theorem v06_sealed_holdout_0379
    (P00 P02 P03 P04 P05 P06 P07 P09 P16 P17 P19 P21 P25 P27 P28 P30 : Point)
    (L00 : Line)
    (h00 : directed_angle_eq_mod_2pi P19 P00 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : between P04 P05 P06)
    (h03 : between P05 P04 P03)
    (h04 : angle_bisector_line P27 P16 P17 P28 L00)
    : directed_angle_eq_mod_2pi P19 P00 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0379
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0379

theorem v06_sealed_holdout_0380
    (P00 P05 P06 P07 P08 P09 P11 P12 P13 P14 P15 P16 P17 P19 P23 P26 P28 : Point)
    (L26 : Line)
    (C19 C20 : Circle)
    (h00 : circle_through_three_noncollinear_points P08 P11 P16 C19)
    (h01 : area_le P06 P19 P00 P13 P26 P07)
    (h02 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h03 : area_le P12 P13 P14 P15 P16 P17)
    (h04 : line_circle_intersection P19 L26 C20)
    : triangle_pred P08 P11 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0380
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0380

theorem v06_sealed_holdout_0381
    (P02 P03 P06 P11 P19 P22 P25 P28 P29 P31 : Point)
    (L18 : Line)
    (C02 C06 C18 C26 : Circle)
    (h00 : equilateral P29 P11 P06)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : line_circle_intersection P03 L18 C26)
    (h03 : area_le P19 P22 P25 P28 P31 P02)
    (h04 : circle_circle_intersection P03 C26 C18)
    : triangle_pred P29 P11 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0381
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0381

theorem v06_sealed_holdout_0382
    (P03 P04 P06 P10 P12 P13 P16 P17 P18 P23 P26 P27 P28 P29 P31 : Point)
    (L00 : Line)
    (h00 : equilateral P03 P10 P06)
    (h01 : between P23 P18 P13)
    (h02 : between P26 P31 P04)
    (h03 : between P29 P12 P27)
    (h04 : angle_bisector_line P03 P16 P17 P28 L00)
    : triangle_pred P03 P10 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0382
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0382

theorem v06_sealed_holdout_0383
    (P04 P06 P07 P10 P11 P16 P17 P19 P21 P27 P31 : Point)
    (L24 L28 : Line)
    (C02 C22 : Circle)
    (h00 : equilateral P31 P11 P06)
    (h01 : angle_bisector_line P16 P07 P17 P27 L28)
    (h02 : angle_bisector_line P21 P10 P16 P27 L24)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : midpoint P04 P21 P06)
    : triangle_pred P31 P11 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0383
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0383

theorem v06_sealed_holdout_0384
    (P00 P02 P03 P04 P05 P06 P08 P11 P12 P17 P23 P26 P30 : Point)
    (h00 : equilateral P00 P11 P06)
    (h01 : midpoint P02 P23 P12)
    (h02 : midpoint P05 P04 P03)
    (h03 : between P08 P17 P26)
    (h04 : between P11 P30 P17)
    : triangle_pred P00 P11 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0384
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0384

theorem v06_sealed_holdout_0385
    (P00 P05 P07 P08 P09 P12 P13 P14 P15 P18 P23 P26 P27 P28 : Point)
    (RF52 : Reflection)
    (h00 : midpoint P14 P27 P08)
    (h01 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h02 : between P12 P13 P14)
    (h03 : midpoint P15 P26 P05)
    (h04 : between P18 P07 P28)
    : reflection_image RF52 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0385
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0385

theorem v06_sealed_holdout_0386
    (P02 P03 P04 P07 P10 P16 P19 P21 P22 P23 P25 P27 P28 P29 P31 : Point)
    (L00 : Line)
    (HOM25 : Homothety)
    (h00 : between P21 P04 P19)
    (h01 : angle_bisector_line P19 P07 P16 P27 L00)
    (h02 : area_le P19 P22 P25 P28 P31 P02)
    (h03 : area_le P22 P03 P16 P29 P10 P23)
    (h04 : midpoint P25 P16 P07)
    : homothety_image HOM25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0386
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0386

theorem v06_sealed_holdout_0387
    (P00 P03 P04 P09 P12 P13 P14 P15 P16 P17 P18 P19 P23 P26 P27 P28 P29 P30 P31 : Point)
    (L00 : Line)
    (INV02 : Inversion)
    (h00 : area_le P28 P13 P30 P15 P00 P17)
    (h01 : midpoint P23 P18 P13)
    (h02 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    (h03 : between P29 P12 P27)
    (h04 : angle_bisector_line P03 P17 P16 P27 L00)
    : inversion_image INV02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0387
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0387

theorem v06_sealed_holdout_0388
    (P01 P02 P03 P07 P08 P09 P14 P15 P19 P22 P24 P27 P28 P29 P30 : Point)
    (L18 : Line)
    (C18 : Circle)
    (SP47 : SpiralSimilarity)
    (h00 : directed_angle_eq_mod_pi P03 P22 P09 P28 P15 P02)
    (h01 : midpoint P30 P27 P24)
    (h02 : midpoint P01 P08 P15)
    (h03 : line_circle_intersection P03 L18 C18)
    (h04 : directed_angle_eq_mod_pi P07 P02 P29 P24 P19 P14)
    : spiral_similarity_center SP47 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0388
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0388

theorem v06_sealed_holdout_0389
    (P08 P11 P14 P19 P23 P25 P27 P31 : Point)
    (L13 : Line)
    (C17 : Circle)
    (h00 : P25 = P08)
    (h01 : P11 = P19)
    (h02 : P27 = P31)
    (h03 : line_circle_intersection P23 L13 C17)
    (h04 : between P14 P11 P08)
    : rotation_preserves_collinear P25 P11 P27 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0389
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0389

theorem v06_sealed_holdout_0390
    (P02 P03 P12 P13 P14 P19 P30 : Point)
    (L10 : Line)
    (C02 C10 C14 C15 C18 C24 : Circle)
    (h00 : circle_with_center_through_point P02 P30 C15)
    (h01 : between P12 P13 P14)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : line_circle_intersection P19 L10 C24)
    : on_circle P30 C15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0390
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0390

theorem v06_sealed_holdout_0391
    (P01 P02 P03 P14 P16 P19 P22 P23 P27 P28 P29 P30 : Point)
    (L20 : Line)
    (C02 C17 C30 : Circle)
    (h00 : circle_through_three_noncollinear_points P23 P01 P30 C17)
    (h01 : circle_circle_intersection P19 C30 C02)
    (h02 : between P22 P03 P16)
    (h03 : angle_bisector_line P02 P14 P16 P27 L20)
    (h04 : midpoint P28 P29 P30)
    : on_circle P23 C17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0391
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0391

theorem v06_sealed_holdout_0392
    (P03 P06 P07 P08 P09 P10 P12 P14 P15 P16 P18 P25 P27 P28 P29 : Point)
    (L00 L08 L21 : Line)
    (C17 : Circle)
    (h00 : line_circle_intersection P28 L21 C17)
    (h01 : angle_bisector_line P25 P07 P16 P27 L08)
    (h02 : directed_angle_eq_mod_pi P29 P12 P27 P10 P25 P08)
    (h03 : angle_bisector_line P03 P14 P16 P27 L00)
    (h04 : area_le P03 P06 P09 P12 P15 P18)
    : on_circle P28 C17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0392
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0392

theorem v06_sealed_holdout_0393
    (P02 P04 P06 P07 P10 P14 P15 P19 P20 P21 P24 P25 P29 : Point)
    (C02 C22 C28 : Circle)
    (h00 : chord P25 P29 C28)
    (h01 : circle_circle_intersection P19 C22 C02)
    (h02 : midpoint P04 P21 P06)
    (h03 : area_le P07 P02 P29 P24 P19 P14)
    (h04 : between P10 P15 P20)
    : on_circle P25 C28 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0393
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0393

theorem v06_sealed_holdout_0394
    (P02 P05 P06 P08 P11 P13 P14 P16 P17 P20 P24 P26 P27 P30 P31 : Point)
    (L24 L26 : Line)
    (C22 : Circle)
    (h00 : tangent_chord_angle P02 P05 P26 L26 C22)
    (h01 : midpoint P08 P17 P26)
    (h02 : between P11 P30 P17)
    (h03 : angle_bisector_line P05 P14 P16 P27 L24)
    (h04 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    : on_circle P26 C22 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0394
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0394

theorem v06_sealed_holdout_0395
    (P01 P04 P05 P06 P07 P10 P12 P14 P16 P17 P18 P19 P20 P21 P23 P24 P26 P27 P28 : Point)
    (L31 : Line)
    (h00 : altitude P04 P14 P12 P23 L31)
    (h01 : area_le P18 P07 P28 P17 P06 P27)
    (h02 : area_le P21 P20 P19 P18 P17 P16)
    (h03 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    (h04 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    : on_line P12 L31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0395
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0395

theorem v06_sealed_holdout_0396
    (P00 P01 P03 P10 P12 P15 P16 P19 P21 P22 P23 P28 P29 P30 P31 : Point)
    (L25 : Line)
    (C02 C22 : Circle)
    (h00 : altitude P00 P15 P12 P23 L25)
    (h01 : midpoint P22 P03 P16)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : area_le P28 P29 P30 P31 P00 P01)
    (h04 : midpoint P31 P10 P21)
    : on_line P12 L25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0396
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0396

theorem v06_sealed_holdout_0397
    (P00 P03 P06 P18 P19 P21 P29 : Point)
    (L00 L26 : Line)
    (C02 C06 C12 C18 : Circle)
    (h00 : angle_bisector_line P21 P19 P18 P29 L00)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : line_circle_intersection P19 L26 C12)
    (h04 : midpoint P06 P19 P00)
    : on_line P21 L00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0397
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0397

theorem v06_sealed_holdout_0398
    (P02 P03 P07 P10 P14 P15 P16 P17 P19 P20 P24 P25 P27 P29 P30 : Point)
    (L04 L18 L26 : Line)
    (C12 C18 : Circle)
    (h00 : line_circle_intersection P14 L26 C12)
    (h01 : line_circle_intersection P03 L18 C18)
    (h02 : directed_angle_eq_mod_pi P07 P02 P29 P24 P19 P14)
    (h03 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    (h04 : angle_bisector_line P14 P17 P16 P27 L04)
    : on_line P14 L26 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0398
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0398

theorem v06_sealed_holdout_0399
    (P00 P03 P05 P08 P11 P17 P19 P20 P22 P27 P30 : Point)
    (C02 C18 C22 C26 : Circle)
    (h00 : equilateral P27 P08 P00)
    (h01 : midpoint P11 P30 P17)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : midpoint P20 P05 P22)
    : equal_length P27 P08 P08 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0399
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0399

theorem v06_sealed_holdout_0400
    (P00 P01 P02 P03 P07 P09 P13 P14 P16 P17 P18 P19 P20 P21 P23 P26 P27 P29 : Point)
    (C02 C18 : Circle)
    (h00 : length_sum P00 P26 P29 P09 P16 P23)
    (h01 : between P23 P02 P13)
    (h02 : area_le P21 P20 P19 P18 P17 P16)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : area_le P27 P14 P01 P20 P07 P26)
    : length_sum P29 P09 P00 P26 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0400
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0400

theorem v06_sealed_holdout_0401
    (P03 P05 P06 P11 P15 P16 P18 P19 P24 P27 P29 P30 P31 : Point)
    (C02 C10 C14 C18 : Circle)
    (h00 : equal_length P29 P05 P15 P27)
    (h01 : equal_length P15 P27 P06 P16)
    (h02 : area_le P30 P11 P24 P05 P18 P31)
    (h03 : circle_circle_intersection P19 C14 C02)
    (h04 : circle_circle_intersection P03 C10 C18)
    : equal_length P29 P05 P06 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0401
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0401

theorem v06_sealed_holdout_0402
    (P00 P01 P02 P03 P05 P06 P08 P12 P13 P16 P18 P19 P20 P21 P23 P24 : Point)
    (C02 C22 : Circle)
    (h00 : area_eq P18 P08 P21 P01 P12 P23)
    (h01 : area_eq P01 P12 P23 P02 P13 P24)
    (h02 : directed_angle_eq_mod_pi P05 P20 P03 P18 P01 P16)
    (h03 : between P06 P19 P00)
    (h04 : circle_circle_intersection P19 C22 C02)
    : area_eq P18 P08 P21 P02 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0402
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0402

theorem v06_sealed_holdout_0403
    (P03 P05 P06 P15 P16 P19 P27 P31 : Point)
    (L31 : Line)
    (C02 C06 C18 C31 : Circle)
    (h00 : equal_length P31 P05 P15 P27)
    (h01 : equal_length P15 P27 P06 P16)
    (h02 : line_circle_intersection P31 L31 C31)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : circle_circle_intersection P03 C02 C18)
    : equal_length P31 P05 P06 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0403
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0403

theorem v06_sealed_holdout_0404
    (P05 P07 P08 P09 P12 P16 P19 P20 P22 P24 P26 P27 : Point)
    (L24 L30 : Line)
    (C02 C14 C22 : Circle)
    (h00 : tangent_chord_angle P12 P05 P26 L30 C02)
    (h01 : angle_bisector_line P05 P08 P16 P27 L24)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : directed_angle_eq_mod_pi P20 P05 P22 P07 P24 P09)
    (h04 : circle_circle_intersection P19 C14 C02)
    : on_circle P26 C02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0404
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0404

theorem v06_sealed_holdout_0405
    (P01 P03 P10 P14 P15 P17 P18 P19 P20 P21 P23 P24 P27 P30 : Point)
    (L18 : Line)
    (h00 : angle_bisector_line P17 P23 P24 P03 L18)
    (h01 : between P21 P20 P19)
    (h02 : between P24 P01 P10)
    (h03 : midpoint P27 P14 P01)
    (h04 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    : angle_bisector P17 P23 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0405
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0405

theorem v06_sealed_holdout_0406
    (P00 P01 P02 P03 P04 P05 P07 P11 P12 P15 P16 P23 P24 P26 P27 P30 P31 : Point)
    (L12 : Line)
    (C10 C18 : Circle)
    (h00 : directed_angle_eq_mod_pi P26 P30 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : angle_bisector_line P12 P11 P16 P27 L12)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : area_le P05 P04 P03 P02 P01 P00)
    : directed_angle_eq_mod_pi P26 P30 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0406
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0406

theorem v06_sealed_holdout_0407
    (P00 P01 P02 P03 P07 P08 P09 P15 P16 P21 P23 P25 P26 P30 : Point)
    (L18 : Line)
    (C02 : Circle)
    (h00 : directed_angle_eq_mod_2pi P15 P01 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : between P08 P01 P26)
    (h03 : between P09 P00 P23)
    (h04 : line_circle_intersection P03 L18 C02)
    : directed_angle_eq_mod_2pi P15 P01 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0407
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0407

theorem v06_sealed_holdout_0408
    (P02 P03 P07 P09 P11 P13 P15 P16 P19 P20 P22 P23 P24 P25 P26 P27 P28 P30 P31 : Point)
    (h00 : directed_angle_eq_mod_pi P28 P30 P03 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : directed_angle_eq_mod_pi P13 P28 P11 P26 P09 P24)
    (h03 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    (h04 : area_le P19 P22 P25 P28 P31 P02)
    : directed_angle_eq_mod_pi P28 P30 P03 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0408
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0408

theorem v06_sealed_holdout_0409
    (P01 P02 P04 P07 P09 P10 P13 P16 P17 P19 P21 P22 P25 P26 P30 P31 : Point)
    (C02 C14 : Circle)
    (h00 : directed_angle_eq_mod_2pi P17 P01 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : directed_angle_eq_mod_pi P22 P19 P16 P13 P10 P07)
    (h03 : circle_circle_intersection P19 C14 C02)
    (h04 : between P26 P31 P04)
    : directed_angle_eq_mod_2pi P17 P01 P09 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0409
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0409

theorem v06_sealed_holdout_0410
    (P01 P06 P08 P11 P12 P14 P16 P19 P24 P27 P30 : Point)
    (L00 L10 : Line)
    (C00 C05 : Circle)
    (h00 : circle_through_three_noncollinear_points P06 P12 P16 C05)
    (h01 : angle_bisector_line P11 P08 P16 P27 L00)
    (h02 : between P27 P14 P01)
    (h03 : between P30 P27 P24)
    (h04 : line_circle_intersection P19 L10 C00)
    : triangle_pred P06 P12 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0410
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0410

theorem v06_sealed_holdout_0411
    (P00 P02 P06 P10 P11 P12 P16 P17 P19 P21 P22 P23 P27 P28 P31 : Point)
    (L00 : Line)
    (C02 C06 : Circle)
    (h00 : equilateral P27 P12 P06)
    (h01 : area_le P31 P10 P21 P00 P11 P22)
    (h02 : between P02 P23 P12)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : angle_bisector_line P27 P17 P16 P28 L00)
    : triangle_pred P27 P12 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0411
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0411

theorem v06_sealed_holdout_0412
    (P00 P03 P05 P08 P09 P12 P13 P15 P16 P23 P26 P27 : Point)
    (L24 : Line)
    (C18 C19 : Circle)
    (h00 : circle_through_three_noncollinear_points P08 P12 P16 C19)
    (h01 : angle_bisector_line P13 P08 P16 P27 L24)
    (h02 : midpoint P09 P00 P23)
    (h03 : circle_circle_intersection P03 C18 C19)
    (h04 : between P15 P26 P05)
    : triangle_pred P08 P12 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0412
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0412

theorem v06_sealed_holdout_0413
    (P03 P06 P09 P10 P11 P12 P13 P14 P16 P19 P22 P23 P24 P26 P27 P28 P29 : Point)
    (L00 L28 : Line)
    (h00 : equilateral P29 P12 P06)
    (h01 : directed_angle_eq_mod_pi P13 P28 P11 P26 P09 P24)
    (h02 : angle_bisector_line P19 P11 P16 P27 L00)
    (h03 : angle_bisector_line P24 P14 P16 P27 L28)
    (h04 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    : triangle_pred P29 P12 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0413
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0413

theorem v06_sealed_holdout_0414
    (P03 P06 P08 P12 P13 P14 P15 P16 P18 P23 P25 P27 P29 P30 : Point)
    (L08 L16 : Line)
    (h00 : equilateral P30 P12 P06)
    (h01 : angle_bisector_line P15 P08 P16 P27 L16)
    (h02 : area_le P23 P18 P13 P08 P03 P30)
    (h03 : angle_bisector_line P25 P14 P16 P27 L08)
    (h04 : midpoint P29 P12 P27)
    : triangle_pred P30 P12 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0414
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0414

theorem v06_sealed_holdout_0415
    (P00 P01 P03 P04 P06 P07 P08 P09 P13 P14 P18 P19 P20 P21 P23 P25 P26 P27 : Point)
    (L02 : Line)
    (C02 C14 C22 : Circle)
    (RF06 : Reflection)
    (h00 : area_le P00 P09 P18 P27 P04 P13)
    (h01 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    (h02 : line_circle_intersection P03 L02 C14)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    : reflection_image RF06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0415
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0415

theorem v06_sealed_holdout_0416
    (P00 P01 P02 P03 P04 P05 P07 P08 P10 P11 P12 P17 P18 P19 P22 P23 P26 P29 P30 : Point)
    (HOM39 : Homothety)
    (h00 : directed_angle_eq_mod_pi P07 P18 P29 P08 P19 P30)
    (h01 : directed_angle_eq_mod_pi P02 P23 P12 P01 P22 P11)
    (h02 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    (h03 : midpoint P08 P17 P26)
    (h04 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    : homothety_image HOM39 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0416
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0416

theorem v06_sealed_holdout_0417
    (P06 P07 P12 P13 P14 P15 P16 P17 P18 P19 P27 P28 : Point)
    (L10 L17 L26 : Line)
    (C13 C16 C20 : Circle)
    (INV12 : Inversion)
    (h00 : line_circle_intersection P07 L17 C13)
    (h01 : line_circle_intersection P19 L10 C16)
    (h02 : area_le P12 P13 P14 P15 P16 P17)
    (h03 : line_circle_intersection P19 L26 C20)
    (h04 : area_le P18 P07 P28 P17 P06 P27)
    : inversion_image INV12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0417
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0417

theorem v06_sealed_holdout_0418
    (P03 P07 P11 P12 P16 P19 P21 P24 P25 P27 P30 : Point)
    (L18 L28 : Line)
    (C02 C06 C18 C26 : Circle)
    (SP53 : SpiralSimilarity)
    (h00 : circle_circle_intersection P19 C06 C02)
    (h01 : line_circle_intersection P03 L18 C26)
    (h02 : angle_bisector_line P24 P11 P16 P27 L28)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    : spiral_similarity_center SP53 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0418
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0418

theorem v06_sealed_holdout_0419
    (P03 P08 P12 P13 P15 P18 P19 P23 P27 P31 : Point)
    (L12 : Line)
    (C02 C18 : Circle)
    (h00 : P23 = P08)
    (h01 : P12 = P19)
    (h02 : P27 = P31)
    (h03 : angle_bisector_line P15 P18 P31 P13 L12)
    (h04 : circle_circle_intersection P03 C02 C18)
    : rotation_preserves_collinear P23 P12 P27 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0419
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0419

theorem v06_sealed_holdout_0420
    (P00 P15 P16 P18 P19 P21 P24 P27 P30 P31 : Point)
    (L10 L16 : Line)
    (C00 C02 C14 C19 : Circle)
    (h00 : circle_with_center_through_point P00 P30 C19)
    (h01 : area_le P30 P27 P24 P21 P18 P15)
    (h02 : line_circle_intersection P19 L10 C00)
    (h03 : angle_bisector_line P31 P15 P16 P27 L16)
    (h04 : circle_circle_intersection P19 C14 C02)
    : on_circle P30 C19 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0420
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0420

theorem v06_sealed_holdout_0421
    (P02 P03 P04 P08 P10 P11 P12 P17 P19 P21 P23 P26 P30 : Point)
    (C02 C06 C18 C19 C26 : Circle)
    (h00 : circle_through_three_noncollinear_points P21 P02 P30 C19)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : directed_angle_eq_mod_pi P08 P17 P26 P03 P12 P21)
    (h03 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h04 : circle_circle_intersection P03 C26 C18)
    : on_circle P21 C19 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0421
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0421

theorem v06_sealed_holdout_0422
    (P01 P03 P05 P07 P10 P16 P17 P18 P19 P20 P21 P24 P27 P28 P29 : Point)
    (L02 L12 : Line)
    (C04 C06 : Circle)
    (h00 : chord P27 P29 C04)
    (h01 : angle_bisector_line P28 P07 P17 P29 L12)
    (h02 : line_circle_intersection P03 L02 C06)
    (h03 : area_le P21 P20 P19 P18 P17 P16)
    (h04 : area_le P24 P01 P10 P19 P28 P05)
    : on_circle P27 C04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0422
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0422

theorem v06_sealed_holdout_0423
    (P00 P01 P02 P03 P07 P10 P12 P16 P19 P21 P22 P23 P25 P28 P29 P30 P31 : Point)
    (C04 : Circle)
    (h00 : chord P23 P30 C04)
    (h01 : area_le P19 P22 P25 P28 P31 P02)
    (h02 : area_le P22 P03 P16 P29 P10 P23)
    (h03 : area_le P25 P16 P07 P30 P21 P12)
    (h04 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    : on_circle P23 C04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0423
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0423

theorem v06_sealed_holdout_0424
    (P00 P03 P06 P07 P09 P11 P12 P13 P15 P17 P18 P19 P26 P28 : Point)
    (L00 L10 L17 : Line)
    (C04 C08 : Circle)
    (h00 : line_circle_intersection P13 L17 C04)
    (h01 : line_circle_intersection P19 L10 C08)
    (h02 : angle_bisector_line P03 P11 P17 P28 L00)
    (h03 : directed_angle_eq_mod_pi P03 P06 P09 P12 P15 P18)
    (h04 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    : on_line P13 L17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0424
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0424

theorem v06_sealed_holdout_0425
    (P01 P02 P04 P06 P07 P08 P09 P15 P16 P18 P21 P23 P25 P27 P29 : Point)
    (L08 L15 : Line)
    (C04 : Circle)
    (h00 : line_circle_intersection P09 L15 C04)
    (h01 : midpoint P01 P08 P15)
    (h02 : area_le P04 P21 P06 P23 P08 P25)
    (h03 : between P07 P02 P29)
    (h04 : angle_bisector_line P09 P18 P16 P27 L08)
    : on_line P09 L15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0425
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0425

theorem v06_sealed_holdout_0426
    (P04 P05 P06 P08 P10 P11 P13 P14 P17 P19 P20 P22 P23 P24 P29 P30 P31 : Point)
    (L08 : Line)
    (h00 : angle_bisector_line P23 P19 P20 P29 L08)
    (h01 : area_le P11 P30 P17 P04 P23 P10)
    (h02 : between P14 P11 P08)
    (h03 : area_le P17 P24 P31 P06 P13 P20)
    (h04 : between P20 P05 P22)
    : on_line P23 L08 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0426
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0426

theorem v06_sealed_holdout_0427
    (P01 P03 P08 P10 P16 P17 P18 P19 P20 P21 P24 P27 P28 P29 : Point)
    (L02 L04 L12 : Line)
    (C06 : Circle)
    (h00 : angle_bisector_line P19 P20 P18 P29 L04)
    (h01 : angle_bisector_line P28 P08 P16 P27 L12)
    (h02 : line_circle_intersection P03 L02 C06)
    (h03 : area_le P21 P20 P19 P18 P17 P16)
    (h04 : between P24 P01 P10)
    : on_line P19 L04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0427
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0427

theorem v06_sealed_holdout_0428
    (P03 P07 P10 P12 P16 P21 P25 P31 : Point)
    (L28 : Line)
    (C18 C19 C26 C28 : Circle)
    (h00 : line_circle_intersection P12 L28 C28)
    (h01 : circle_circle_intersection P03 C26 C18)
    (h02 : between P25 P16 P07)
    (h03 : circle_circle_intersection P03 C18 C19)
    (h04 : midpoint P31 P10 P21)
    : on_line P12 L28 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0428
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0428

theorem v06_sealed_holdout_0429
    (P00 P03 P09 P12 P13 P16 P18 P19 P25 P27 P29 : Point)
    (L00 L24 L26 : Line)
    (C12 : Circle)
    (h00 : equilateral P25 P09 P00)
    (h01 : between P29 P12 P27)
    (h02 : angle_bisector_line P03 P12 P16 P27 L00)
    (h03 : line_circle_intersection P19 L26 C12)
    (h04 : angle_bisector_line P13 P18 P16 P27 L24)
    : equal_length P25 P09 P09 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0429
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0429

theorem v06_sealed_holdout_0430
    (P02 P05 P07 P09 P10 P11 P12 P13 P15 P16 P20 P23 P24 P26 P27 P28 P29 P30 P31 : Point)
    (h00 : length_sum P30 P27 P31 P09 P16 P23)
    (h01 : directed_angle_eq_mod_pi P09 P16 P23 P30 P05 P12)
    (h02 : midpoint P07 P02 P29)
    (h03 : between P10 P15 P20)
    (h04 : directed_angle_eq_mod_pi P13 P28 P11 P26 P09 P24)
    : length_sum P31 P09 P30 P27 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0430
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0430

theorem v06_sealed_holdout_0431
    (P05 P06 P13 P15 P16 P17 P20 P22 P24 P27 P28 P31 : Point)
    (L03 : Line)
    (C27 : Circle)
    (h00 : equal_length P27 P05 P15 P28)
    (h01 : equal_length P15 P28 P06 P16)
    (h02 : line_circle_intersection P15 L03 C27)
    (h03 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    (h04 : midpoint P20 P05 P22)
    : equal_length P27 P05 P06 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0431
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0431

theorem v06_sealed_holdout_0432
    (P01 P02 P05 P09 P10 P12 P13 P16 P19 P21 P23 P24 P27 P28 : Point)
    (L26 : Line)
    (C10 C22 C28 : Circle)
    (h00 : area_eq P16 P09 P21 P01 P12 P23)
    (h01 : area_eq P01 P12 P23 P02 P13 P24)
    (h02 : circle_circle_intersection P27 C22 C10)
    (h03 : area_le P24 P01 P10 P19 P28 P05)
    (h04 : line_circle_intersection P19 L26 C28)
    : area_eq P16 P09 P21 P02 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0432
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0432

theorem v06_sealed_holdout_0433
    (P00 P05 P06 P10 P11 P13 P15 P16 P17 P18 P19 P21 P22 P27 P29 P31 : Point)
    (L08 L28 : Line)
    (h00 : equal_length P29 P06 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : angle_bisector_line P29 P19 P31 P13 L28)
    (h03 : area_le P31 P10 P21 P00 P11 P22)
    (h04 : angle_bisector_line P17 P18 P16 P27 L08)
    : equal_length P29 P06 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0433
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0433

theorem v06_sealed_holdout_0434
    (P03 P06 P09 P10 P12 P15 P16 P18 P19 P26 P27 : Point)
    (L00 L10 L20 : Line)
    (C06 C18 C26 : Circle)
    (h00 : tangent_chord_angle P10 P06 P26 L10 C06)
    (h01 : angle_bisector_line P03 P09 P16 P27 L00)
    (h02 : area_le P03 P06 P09 P12 P15 P18)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : angle_bisector_line P18 P19 P16 P27 L20)
    : on_circle P26 C06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0434
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0434

theorem v06_sealed_holdout_0435
    (P02 P03 P07 P09 P10 P11 P13 P15 P16 P20 P23 P24 P25 P28 P29 P30 : Point)
    (L20 : Line)
    (h00 : angle_bisector_line P15 P23 P24 P03 L20)
    (h01 : midpoint P07 P02 P29)
    (h02 : area_le P10 P15 P20 P25 P30 P03)
    (h03 : midpoint P13 P28 P11)
    (h04 : between P16 P09 P02)
    : angle_bisector P15 P23 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0435
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0435

theorem v06_sealed_holdout_0436
    (P00 P03 P04 P07 P08 P13 P15 P16 P18 P19 P23 P24 P25 P30 P31 : Point)
    (L10 : Line)
    (C00 C18 C19 : Circle)
    (h00 : directed_angle_eq_mod_pi P24 P31 P04 P15 P23 P00)
    (h01 : directed_angle_eq_mod_pi P15 P23 P00 P07 P16 P25)
    (h02 : line_circle_intersection P19 L10 C00)
    (h03 : circle_circle_intersection P03 C18 C19)
    (h04 : area_le P23 P18 P13 P08 P03 P30)
    : directed_angle_eq_mod_pi P24 P31 P04 P07 P16 P25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0436
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0436

theorem v06_sealed_holdout_0437
    (P01 P02 P03 P04 P07 P09 P13 P14 P15 P16 P21 P24 P25 P26 P27 P30 : Point)
    (h00 : directed_angle_eq_mod_2pi P13 P02 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P03)
    (h02 : directed_angle_eq_mod_pi P26 P15 P04 P25 P14 P03)
    (h03 : midpoint P27 P14 P01)
    (h04 : midpoint P30 P27 P24)
    : directed_angle_eq_mod_2pi P13 P02 P09 P16 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0437
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0437

theorem v06_sealed_holdout_0438
    (P00 P01 P02 P03 P04 P05 P07 P10 P11 P12 P15 P16 P21 P22 P23 P24 P26 P31 : Point)
    (h00 : directed_angle_eq_mod_pi P26 P31 P04 P15 P23 P00)
    (h01 : directed_angle_eq_mod_pi P15 P23 P00 P07 P16 P24)
    (h02 : area_le P31 P10 P21 P00 P11 P22)
    (h03 : between P02 P23 P12)
    (h04 : area_le P05 P04 P03 P02 P01 P00)
    : directed_angle_eq_mod_pi P26 P31 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0438
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0438

theorem v06_sealed_holdout_0439
    (P02 P03 P07 P09 P12 P13 P14 P15 P16 P19 P21 P25 P30 : Point)
    (C02 C14 C22 C30 : Circle)
    (h00 : directed_angle_eq_mod_2pi P15 P02 P09 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P03)
    (h02 : circle_circle_intersection P15 C14 C30)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : midpoint P12 P13 P14)
    : directed_angle_eq_mod_2pi P15 P02 P09 P16 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0439
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0439

theorem v06_sealed_holdout_0440
    (P02 P03 P04 P09 P10 P11 P13 P15 P16 P18 P20 P24 P25 P27 P28 P30 : Point)
    (L28 : Line)
    (C23 : Circle)
    (h00 : circle_through_three_noncollinear_points P04 P13 P16 C23)
    (h01 : area_le P10 P15 P20 P25 P30 P03)
    (h02 : midpoint P13 P28 P11)
    (h03 : between P16 P09 P02)
    (h04 : angle_bisector_line P24 P18 P16 P27 L28)
    : triangle_pred P04 P13 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0440
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0440

theorem v06_sealed_holdout_0441
    (P05 P06 P07 P09 P13 P16 P17 P18 P20 P22 P23 P24 P25 P27 P31 : Point)
    (L08 : Line)
    (h00 : equilateral P25 P13 P06)
    (h01 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    (h02 : area_le P20 P05 P22 P07 P24 P09)
    (h03 : midpoint P23 P18 P13)
    (h04 : angle_bisector_line P25 P18 P16 P27 L08)
    : triangle_pred P25 P13 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0441
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0441

theorem v06_sealed_holdout_0442
    (P01 P06 P07 P08 P10 P13 P14 P15 P16 P20 P24 P26 P27 P30 : Point)
    (C05 : Circle)
    (h00 : circle_through_three_noncollinear_points P06 P13 P16 C05)
    (h01 : midpoint P24 P01 P10)
    (h02 : area_le P27 P14 P01 P20 P07 P26)
    (h03 : between P30 P27 P24)
    (h04 : midpoint P01 P08 P15)
    : triangle_pred P06 P13 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0442
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0442

theorem v06_sealed_holdout_0443
    (P01 P02 P03 P04 P05 P06 P08 P10 P11 P12 P13 P17 P21 P22 P23 P26 P27 P31 : Point)
    (h00 : equilateral P27 P13 P06)
    (h01 : between P31 P10 P21)
    (h02 : directed_angle_eq_mod_pi P02 P23 P12 P01 P22 P11)
    (h03 : between P05 P04 P03)
    (h04 : between P08 P17 P26)
    : triangle_pred P27 P13 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0443
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0443

theorem v06_sealed_holdout_0444
    (P00 P03 P05 P06 P09 P12 P13 P14 P16 P18 P23 P27 P28 : Point)
    (L02 L12 : Line)
    (C30 : Circle)
    (h00 : equilateral P28 P13 P06)
    (h01 : line_circle_intersection P03 L02 C30)
    (h02 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h03 : midpoint P12 P13 P14)
    (h04 : angle_bisector_line P28 P18 P16 P27 L12)
    : triangle_pred P28 P13 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0444
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0444

theorem v06_sealed_holdout_0445
    (P03 P11 P12 P13 P15 P16 P19 P22 P23 P24 P27 P28 : Point)
    (L00 L21 L28 : Line)
    (C09 : Circle)
    (RF24 : Reflection)
    (h00 : line_circle_intersection P23 L21 C09)
    (h01 : midpoint P13 P28 P11)
    (h02 : angle_bisector_line P19 P12 P16 P27 L00)
    (h03 : angle_bisector_line P24 P15 P16 P27 L28)
    (h04 : between P22 P03 P16)
    : reflection_image RF24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0445
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0445

theorem v06_sealed_holdout_0446
    (P03 P04 P05 P07 P08 P09 P10 P12 P14 P19 P20 P22 P24 P25 P26 P27 P29 P31 : Point)
    (L26 : Line)
    (C04 C06 C18 : Circle)
    (HOM53 : Homothety)
    (h00 : circle_circle_intersection P03 C06 C18)
    (h01 : area_le P20 P05 P22 P07 P24 P09)
    (h02 : line_circle_intersection P19 L26 C04)
    (h03 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    (h04 : directed_angle_eq_mod_pi P29 P12 P27 P10 P25 P08)
    : homothety_image HOM53 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0446
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0446

theorem v06_sealed_holdout_0447
    (P01 P03 P07 P11 P13 P14 P19 P20 P26 P27 P31 : Point)
    (L10 L12 L18 : Line)
    (C00 C18 C26 : Circle)
    (INV22 : Inversion)
    (h00 : angle_bisector_line P11 P19 P31 P13 L12)
    (h01 : area_le P27 P14 P01 P20 P07 P26)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : line_circle_intersection P19 L10 C00)
    (h04 : line_circle_intersection P03 L18 C18)
    : inversion_image INV22 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0447
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0447

theorem v06_sealed_holdout_0448
    (P01 P02 P03 P07 P11 P12 P17 P18 P19 P22 P23 P29 P30 : Point)
    (L10 L18 : Line)
    (C10 C24 : Circle)
    (SP59 : SpiralSimilarity)
    (h00 : midpoint P07 P18 P29)
    (h01 : area_le P02 P23 P12 P01 P22 P11)
    (h02 : line_circle_intersection P19 L10 C24)
    (h03 : line_circle_intersection P03 L18 C10)
    (h04 : midpoint P11 P30 P17)
    : spiral_similarity_center SP59 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0448
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0448

theorem v06_sealed_holdout_0449
    (P01 P08 P13 P14 P16 P19 P21 P27 P31 : Point)
    (L08 : Line)
    (h00 : P21 = P08)
    (h01 : P13 = P19)
    (h02 : P27 = P31)
    (h03 : between P14 P27 P08)
    (h04 : angle_bisector_line P01 P19 P16 P27 L08)
    : rotation_preserves_collinear P21 P13 P27 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0449
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0449

theorem v06_sealed_holdout_0450
    (P03 P07 P09 P12 P16 P19 P21 P22 P25 P27 P30 P31 : Point)
    (L00 : Line)
    (C18 C23 C26 : Circle)
    (h00 : circle_with_center_through_point P30 P31 C23)
    (h01 : angle_bisector_line P19 P09 P16 P27 L00)
    (h02 : midpoint P19 P22 P25)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : area_le P25 P16 P07 P30 P21 P12)
    : on_circle P31 C23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0450
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0450

theorem v06_sealed_holdout_0451
    (P00 P03 P04 P11 P18 P19 P25 P29 P30 : Point)
    (L02 : Line)
    (C02 C06 C14 C21 C22 : Circle)
    (h00 : circle_through_three_noncollinear_points P19 P03 P30 C21)
    (h01 : circle_circle_intersection P19 C14 C02)
    (h02 : line_circle_intersection P03 L02 C22)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    : on_circle P19 C21 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0451
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0451

theorem v06_sealed_holdout_0452
    (P01 P02 P04 P06 P07 P08 P15 P18 P21 P23 P24 P25 P27 P29 P30 : Point)
    (L21 : Line)
    (C13 : Circle)
    (h00 : line_circle_intersection P24 L21 C13)
    (h01 : area_le P30 P27 P24 P21 P18 P15)
    (h02 : between P01 P08 P15)
    (h03 : area_le P04 P21 P06 P23 P08 P25)
    (h04 : midpoint P07 P02 P29)
    : on_circle P24 C13 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0452
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0452

theorem v06_sealed_holdout_0453
    (P03 P08 P11 P17 P19 P21 P26 P30 P31 : Point)
    (C02 C06 C12 C18 C26 : Circle)
    (h00 : chord P21 P31 C12)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : midpoint P08 P17 P26)
    (h03 : between P11 P30 P17)
    (h04 : circle_circle_intersection P03 C26 C18)
    : on_circle P21 C12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0453
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0453

theorem v06_sealed_holdout_0454
    (P01 P04 P05 P07 P10 P14 P15 P16 P17 P18 P19 P20 P21 P23 P24 P28 : Point)
    (L17 : Line)
    (C02 C30 : Circle)
    (h00 : altitude P04 P15 P14 P23 L17)
    (h01 : between P18 P07 P28)
    (h02 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    (h03 : area_le P24 P01 P10 P19 P28 P05)
    (h04 : circle_circle_intersection P19 C30 C02)
    : on_line P14 L17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0454
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0454

theorem v06_sealed_holdout_0455
    (P00 P01 P02 P03 P07 P12 P16 P19 P21 P22 P25 P28 P29 P30 P31 : Point)
    (L17 : Line)
    (C18 C20 C26 : Circle)
    (h00 : line_circle_intersection P07 L17 C20)
    (h01 : area_le P19 P22 P25 P28 P31 P02)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : area_le P25 P16 P07 P30 P21 P12)
    (h04 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    : on_line P07 L17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0455
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0455

theorem v06_sealed_holdout_0456
    (P00 P03 P04 P06 P09 P11 P12 P14 P15 P17 P18 P19 P23 P25 P26 P28 P29 P31 : Point)
    (L05 L10 : Line)
    (C08 : Circle)
    (h00 : altitude P28 P17 P12 P23 L05)
    (h01 : area_le P26 P31 P04 P09 P14 P19)
    (h02 : line_circle_intersection P19 L10 C08)
    (h03 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    (h04 : directed_angle_eq_mod_pi P03 P06 P09 P12 P15 P18)
    : on_line P12 L05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0456
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0456

theorem v06_sealed_holdout_0457
    (P02 P03 P07 P09 P13 P16 P17 P18 P21 P26 P27 P29 P31 : Point)
    (L02 L08 L16 L20 : Line)
    (C22 : Circle)
    (h00 : angle_bisector_line P17 P21 P18 P29 L08)
    (h01 : angle_bisector_line P26 P09 P16 P27 L20)
    (h02 : angle_bisector_line P31 P13 P16 P27 L16)
    (h03 : between P07 P02 P29)
    (h04 : line_circle_intersection P03 L02 C22)
    : on_line P17 L08 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0457
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0457

theorem v06_sealed_holdout_0458
    (P00 P02 P03 P05 P06 P08 P10 P11 P13 P14 P16 P17 P20 P24 P27 P31 : Point)
    (L18 L28 L30 : Line)
    (C10 C12 : Circle)
    (h00 : line_circle_intersection P10 L30 C12)
    (h01 : line_circle_intersection P03 L18 C10)
    (h02 : angle_bisector_line P00 P13 P16 P27 L28)
    (h03 : directed_angle_eq_mod_pi P14 P11 P08 P05 P02 P31)
    (h04 : area_le P17 P24 P31 P06 P13 P20)
    : on_line P10 L30 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0458
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0458

theorem v06_sealed_holdout_0459
    (P00 P01 P03 P06 P10 P13 P16 P17 P19 P23 P27 : Point)
    (L04 L08 L26 : Line)
    (C02 C18 C20 : Circle)
    (h00 : equilateral P23 P10 P00)
    (h01 : line_circle_intersection P19 L26 C20)
    (h02 : angle_bisector_line P01 P13 P16 P27 L08)
    (h03 : angle_bisector_line P06 P16 P17 P27 L04)
    (h04 : circle_circle_intersection P03 C02 C18)
    : equal_length P23 P10 P10 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0459
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0459

theorem v06_sealed_holdout_0460
    (P00 P01 P07 P09 P10 P11 P16 P21 P23 P25 P28 P29 P30 P31 : Point)
    (C22 C26 : Circle)
    (h00 : length_sum P28 P29 P30 P09 P16 P23)
    (h01 : circle_circle_intersection P11 C22 C26)
    (h02 : between P25 P16 P07)
    (h03 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    (h04 : between P31 P10 P21)
    : length_sum P30 P09 P28 P29 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0460
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0460

theorem v06_sealed_holdout_0461
    (P00 P03 P05 P06 P07 P09 P12 P13 P15 P16 P18 P19 P20 P25 P26 P27 P31 : Point)
    (L28 : Line)
    (h00 : equal_length P25 P06 P15 P27)
    (h01 : equal_length P15 P27 P05 P16)
    (h02 : angle_bisector_line P25 P20 P31 P13 L28)
    (h03 : area_le P03 P06 P09 P12 P15 P18)
    (h04 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    : equal_length P25 P06 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0461
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0461

theorem v06_sealed_holdout_0462
    (P01 P02 P03 P09 P10 P11 P12 P13 P14 P16 P21 P23 P24 P26 P28 : Point)
    (L02 : Line)
    (C22 : Circle)
    (h00 : area_eq P14 P10 P21 P01 P12 P23)
    (h01 : area_eq P01 P12 P23 P02 P13 P24)
    (h02 : midpoint P09 P16 P23)
    (h03 : line_circle_intersection P03 L02 C22)
    (h04 : area_le P13 P28 P11 P26 P09 P24)
    : area_eq P14 P10 P21 P02 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0462
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0462

theorem v06_sealed_holdout_0463
    (P02 P05 P06 P15 P16 P17 P20 P22 P24 P25 P27 P28 P31 : Point)
    (h00 : equal_length P27 P06 P15 P28)
    (h01 : equal_length P15 P28 P05 P16)
    (h02 : between P16 P25 P02)
    (h03 : between P17 P24 P31)
    (h04 : between P20 P05 P22)
    : equal_length P27 P06 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0463
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0463

theorem v06_sealed_holdout_0464
    (P01 P03 P06 P07 P08 P13 P14 P16 P26 P27 : Point)
    (L04 L18 L22 : Line)
    (C10 C18 : Circle)
    (h00 : tangent_chord_angle P08 P07 P26 L22 C10)
    (h01 : circle_circle_intersection P03 C10 C18)
    (h02 : angle_bisector_line P06 P13 P16 P27 L04)
    (h03 : line_circle_intersection P03 L18 C10)
    (h04 : midpoint P27 P14 P01)
    : on_circle P26 C10 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0464
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0464

theorem v06_sealed_holdout_0465
    (P00 P01 P02 P03 P07 P11 P12 P13 P16 P19 P21 P22 P23 P24 P25 P28 P29 P30 P31 : Point)
    (L22 : Line)
    (C02 C14 : Circle)
    (h00 : angle_bisector_line P13 P24 P25 P03 L22)
    (h01 : area_le P25 P16 P07 P30 P21 P12)
    (h02 : area_le P28 P29 P30 P31 P00 P01)
    (h03 : circle_circle_intersection P19 C14 C02)
    (h04 : area_le P02 P23 P12 P01 P22 P11)
    : angle_bisector P13 P24 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0465
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0465

theorem v06_sealed_holdout_0466
    (P00 P04 P06 P07 P08 P09 P13 P15 P16 P19 P22 P23 P24 P26 P27 P31 : Point)
    (L28 : Line)
    (h00 : directed_angle_eq_mod_pi P22 P31 P04 P15 P23 P00)
    (h01 : directed_angle_eq_mod_pi P15 P23 P00 P07 P16 P24)
    (h02 : angle_bisector_line P08 P13 P16 P27 L28)
    (h03 : area_le P06 P19 P00 P13 P26 P07)
    (h04 : between P09 P00 P23)
    : directed_angle_eq_mod_pi P22 P31 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0466
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0466

theorem v06_sealed_holdout_0467
    (P02 P03 P07 P09 P10 P11 P13 P16 P21 P24 P25 P26 P28 P30 P31 : Point)
    (L18 : Line)
    (C14 C15 C26 : Circle)
    (h00 : directed_angle_eq_mod_2pi P11 P03 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : circle_circle_intersection P31 C14 C15)
    (h03 : area_le P13 P28 P11 P26 P09 P24)
    (h04 : line_circle_intersection P03 L18 C26)
    : directed_angle_eq_mod_2pi P11 P03 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0467
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0467

theorem v06_sealed_holdout_0468
    (P00 P04 P05 P07 P15 P16 P17 P19 P20 P22 P23 P24 P25 P31 : Point)
    (L26 : Line)
    (C04 : Circle)
    (h00 : directed_angle_eq_mod_pi P24 P00 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P25)
    (h02 : between P17 P24 P31)
    (h03 : between P20 P05 P22)
    (h04 : line_circle_intersection P19 L26 C04)
    : directed_angle_eq_mod_pi P24 P00 P04 P07 P16 P25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0468
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0468

theorem v06_sealed_holdout_0469
    (P01 P02 P03 P04 P07 P10 P13 P14 P15 P16 P19 P20 P21 P25 P26 P27 P30 : Point)
    (L24 : Line)
    (h00 : directed_angle_eq_mod_2pi P13 P03 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : midpoint P26 P15 P04)
    (h03 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    (h04 : angle_bisector_line P21 P19 P16 P27 L24)
    : directed_angle_eq_mod_2pi P13 P03 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0469
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0469

theorem v06_sealed_holdout_0470
    (P02 P03 P04 P05 P10 P14 P16 P17 P18 P21 P27 P31 : Point)
    (L08 : Line)
    (C09 C18 C19 : Circle)
    (h00 : circle_through_three_noncollinear_points P02 P14 P16 C09)
    (h01 : circle_circle_intersection P03 C18 C19)
    (h02 : midpoint P31 P10 P21)
    (h03 : angle_bisector_line P17 P16 P18 P27 L08)
    (h04 : between P05 P04 P03)
    : triangle_pred P02 P14 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0470
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0470

theorem v06_sealed_holdout_0471
    (P00 P03 P06 P09 P12 P13 P14 P15 P16 P17 P23 : Point)
    (C18 C26 : Circle)
    (h00 : equilateral P23 P14 P06)
    (h01 : between P03 P06 P09)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : midpoint P09 P00 P23)
    (h04 : area_le P12 P13 P14 P15 P16 P17)
    : triangle_pred P23 P14 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0471
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0471

theorem v06_sealed_holdout_0472
    (P03 P04 P09 P10 P11 P13 P14 P15 P16 P17 P19 P20 P22 P24 P25 P26 P27 P28 P30 : Point)
    (L00 : Line)
    (C23 : Circle)
    (h00 : circle_through_three_noncollinear_points P04 P14 P16 C23)
    (h01 : area_le P10 P15 P20 P25 P30 P03)
    (h02 : area_le P13 P28 P11 P26 P09 P24)
    (h03 : angle_bisector_line P19 P16 P17 P27 L00)
    (h04 : between P19 P22 P25)
    : triangle_pred P04 P14 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0472
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0472

theorem v06_sealed_holdout_0473
    (P03 P06 P13 P14 P17 P18 P20 P23 P24 P25 P31 : Point)
    (C10 C18 C19 : Circle)
    (h00 : equilateral P25 P14 P06)
    (h01 : area_le P17 P24 P31 P06 P13 P20)
    (h02 : circle_circle_intersection P03 C18 C19)
    (h03 : midpoint P23 P18 P13)
    (h04 : circle_circle_intersection P03 C10 C18)
    : triangle_pred P25 P14 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0473
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0473

theorem v06_sealed_holdout_0474
    (P01 P06 P07 P08 P10 P14 P15 P18 P20 P21 P24 P26 P27 P30 : Point)
    (h00 : equilateral P26 P14 P06)
    (h01 : midpoint P24 P01 P10)
    (h02 : area_le P27 P14 P01 P20 P07 P26)
    (h03 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    (h04 : between P01 P08 P15)
    : triangle_pred P26 P14 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0474
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0474

theorem v06_sealed_holdout_0475
    (P00 P01 P02 P03 P04 P05 P07 P08 P10 P12 P13 P16 P17 P20 P21 P23 P26 P27 P31 : Point)
    (L12 : Line)
    (RF42 : Reflection)
    (h00 : angle_bisector_line P07 P20 P31 P13 L12)
    (h01 : angle_bisector_line P12 P10 P16 P27 L12)
    (h02 : between P02 P23 P12)
    (h03 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    (h04 : area_le P08 P17 P26 P03 P12 P21)
    : reflection_image RF42 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0475
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0475

theorem v06_sealed_holdout_0476
    (P00 P03 P05 P06 P09 P11 P12 P13 P14 P15 P16 P17 P23 P26 P27 : Point)
    (C18 C26 : Circle)
    (HOM03 : Homothety)
    (h00 : midpoint P11 P14 P17)
    (h01 : circle_circle_intersection P03 C26 C18)
    (h02 : midpoint P09 P00 P23)
    (h03 : midpoint P12 P13 P14)
    (h04 : area_le P15 P26 P05 P16 P27 P06)
    : homothety_image HOM03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0476
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0476

theorem v06_sealed_holdout_0477
    (P02 P03 P09 P10 P14 P16 P18 P19 P22 P23 P25 P27 P28 P29 P31 : Point)
    (L04 : Line)
    (INV32 : Inversion)
    (h00 : between P18 P23 P28)
    (h01 : angle_bisector_line P14 P10 P16 P27 L04)
    (h02 : between P16 P09 P02)
    (h03 : area_le P19 P22 P25 P28 P31 P02)
    (h04 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    : inversion_image INV32 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0477
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0477

theorem v06_sealed_holdout_0478
    (P00 P04 P07 P10 P13 P14 P15 P16 P19 P20 P21 P25 P26 P27 P28 P31 : Point)
    (L12 L16 : Line)
    (C02 C06 : Circle)
    (SP01 : SpiralSimilarity)
    (h00 : area_le P25 P00 P07 P14 P21 P28)
    (h01 : angle_bisector_line P15 P10 P16 P27 L16)
    (h02 : angle_bisector_line P20 P13 P16 P27 L12)
    (h03 : midpoint P26 P31 P04)
    (h04 : circle_circle_intersection P19 C06 C02)
    : spiral_similarity_center SP01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0478
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0478

theorem v06_sealed_holdout_0479
    (P00 P03 P04 P08 P09 P13 P14 P18 P19 P20 P27 P31 : Point)
    (L18 : Line)
    (C18 : Circle)
    (h00 : P19 = P08)
    (h01 : P14 = P20)
    (h02 : P27 = P31)
    (h03 : directed_angle_eq_mod_pi P00 P09 P18 P27 P04 P13)
    (h04 : line_circle_intersection P03 L18 C18)
    : rotation_preserves_collinear P19 P14 P27 P08 P20 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0479
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0479

theorem v06_sealed_holdout_0480
    (P00 P03 P04 P05 P08 P10 P11 P12 P16 P17 P21 P26 P27 P28 P30 : Point)
    (L08 : Line)
    (C27 : Circle)
    (h00 : circle_with_center_through_point P28 P00 C27)
    (h01 : angle_bisector_line P17 P10 P16 P27 L08)
    (h02 : midpoint P05 P04 P03)
    (h03 : directed_angle_eq_mod_pi P08 P17 P26 P03 P12 P21)
    (h04 : midpoint P11 P30 P17)
    : on_circle P00 C27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0480
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0480

theorem v06_sealed_holdout_0481
    (P03 P05 P07 P15 P16 P17 P18 P19 P20 P21 P26 P28 : Point)
    (L21 : Line)
    (C03 C18 C19 : Circle)
    (h00 : line_circle_intersection P26 L21 C03)
    (h01 : circle_circle_intersection P03 C18 C19)
    (h02 : midpoint P15 P26 P05)
    (h03 : between P18 P07 P28)
    (h04 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    : on_circle P26 C03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0481
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0481

theorem v06_sealed_holdout_0482
    (P02 P03 P16 P17 P19 P22 P23 P25 P28 P31 : Point)
    (L18 L20 : Line)
    (C02 C18 C20 C26 : Circle)
    (h00 : chord P23 P31 C20)
    (h01 : between P19 P22 P25)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : angle_bisector_line P02 P16 P17 P28 L20)
    (h04 : line_circle_intersection P03 L18 C02)
    : on_circle P23 C20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0482
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0482

theorem v06_sealed_holdout_0483
    (P00 P03 P06 P09 P17 P19 P25 P27 P28 : Point)
    (L08 L10 L18 : Line)
    (C02 C06 C18 C26 : Circle)
    (h00 : tangent_chord_angle P00 P06 P27 L10 C18)
    (h01 : angle_bisector_line P25 P09 P17 P28 L08)
    (h02 : circle_circle_intersection P19 C06 C02)
    (h03 : line_circle_intersection P03 L18 C26)
    (h04 : midpoint P03 P06 P09)
    : on_circle P27 C18 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0483
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0483

theorem v06_sealed_holdout_0484
    (P01 P02 P03 P04 P07 P08 P09 P10 P13 P14 P15 P17 P19 P20 P22 P24 P25 P28 P29 P30 P31 : Point)
    (L16 L21 : Line)
    (C04 : Circle)
    (h00 : line_circle_intersection P09 L21 C04)
    (h01 : directed_angle_eq_mod_pi P01 P08 P15 P22 P29 P04)
    (h02 : angle_bisector_line P31 P13 P17 P28 L16)
    (h03 : directed_angle_eq_mod_pi P07 P02 P29 P24 P19 P14)
    (h04 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    : on_line P09 L21 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0484
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0484

theorem v06_sealed_holdout_0485
    (P03 P08 P11 P14 P17 P20 P21 P23 P24 P29 P30 P31 : Point)
    (L18 L20 : Line)
    (C18 : Circle)
    (h00 : angle_bisector_line P23 P20 P21 P29 L20)
    (h01 : midpoint P11 P30 P17)
    (h02 : between P14 P11 P08)
    (h03 : between P17 P24 P31)
    (h04 : line_circle_intersection P03 L18 C18)
    : on_line P23 L20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0485
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0485

theorem v06_sealed_holdout_0486
    (P01 P05 P06 P12 P13 P14 P15 P16 P17 P18 P19 P20 P21 P23 P26 P27 : Point)
    (L08 L11 : Line)
    (h00 : altitude P26 P18 P12 P23 L11)
    (h01 : midpoint P12 P13 P14)
    (h02 : area_le P15 P26 P05 P16 P27 P06)
    (h03 : angle_bisector_line P01 P17 P16 P27 L08)
    (h04 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    : on_line P12 L11 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0486
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0486

theorem v06_sealed_holdout_0487
    (P00 P01 P07 P10 P11 P12 P16 P17 P21 P22 P25 P28 P29 P30 P31 : Point)
    (L02 L24 : Line)
    (C28 : Circle)
    (h00 : line_circle_intersection P12 L02 C28)
    (h01 : angle_bisector_line P29 P10 P17 P28 L24)
    (h02 : area_le P25 P16 P07 P30 P21 P12)
    (h03 : area_le P28 P29 P30 P31 P00 P01)
    (h04 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    : on_line P12 L02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0487
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0487

theorem v06_sealed_holdout_0488
    (P00 P01 P03 P08 P10 P12 P16 P17 P18 P25 P27 P28 P29 : Point)
    (L28 : Line)
    (C18 C26 : Circle)
    (h00 : equilateral P25 P10 P01)
    (h01 : midpoint P29 P12 P27)
    (h02 : midpoint P00 P25 P18)
    (h03 : angle_bisector_line P08 P16 P17 P28 L28)
    (h04 : circle_circle_intersection P03 C26 C18)
    : equal_length P25 P10 P10 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0488
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0488

theorem v06_sealed_holdout_0489
    (P00 P01 P03 P08 P10 P11 P15 P19 P20 P21 : Point)
    (L26 : Line)
    (C04 C18 C19 : Circle)
    (h00 : equilateral P21 P11 P00)
    (h01 : between P01 P08 P15)
    (h02 : circle_circle_intersection P03 C18 C19)
    (h03 : line_circle_intersection P19 L26 C04)
    (h04 : midpoint P10 P15 P20)
    : equal_length P21 P11 P11 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0489
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0489

theorem v06_sealed_holdout_0490
    (P03 P04 P06 P09 P10 P11 P12 P13 P16 P17 P20 P23 P24 P26 P29 P30 P31 : Point)
    (C18 C26 : Circle)
    (h00 : length_sum P26 P29 P30 P09 P16 P23)
    (h01 : midpoint P13 P12 P11)
    (h02 : area_le P11 P30 P17 P04 P23 P10)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : area_le P17 P24 P31 P06 P13 P20)
    : length_sum P30 P09 P26 P29 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0490
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0490

theorem v06_sealed_holdout_0491
    (P01 P05 P07 P10 P15 P16 P19 P20 P21 P22 P23 P24 P27 : Point)
    (C02 C06 : Circle)
    (h00 : equal_length P23 P07 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : between P20 P21 P22)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : between P24 P01 P10)
    : equal_length P23 P07 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0491
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0491

theorem v06_sealed_holdout_0492
    (P01 P02 P03 P04 P07 P10 P11 P12 P13 P14 P19 P22 P23 P24 P27 P28 P29 P30 : Point)
    (L26 : Line)
    (C20 : Circle)
    (h00 : area_eq P12 P11 P22 P02 P13 P23)
    (h01 : area_eq P02 P13 P23 P03 P14 P24)
    (h02 : area_le P27 P30 P01 P04 P07 P10)
    (h03 : midpoint P28 P29 P30)
    (h04 : line_circle_intersection P19 L26 C20)
    : area_eq P12 P11 P22 P03 P14 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0492
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0492

theorem v06_sealed_holdout_0493
    (P02 P03 P05 P06 P07 P09 P12 P13 P15 P16 P17 P20 P22 P25 P27 : Point)
    (L24 : Line)
    (h00 : equal_length P25 P07 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : directed_angle_eq_mod_pi P02 P07 P12 P17 P22 P27)
    (h03 : midpoint P03 P06 P09)
    (h04 : angle_bisector_line P13 P20 P16 P27 L24)
    : equal_length P25 P07 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0493
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0493

theorem v06_sealed_holdout_0494
    (P02 P03 P07 P11 P13 P14 P15 P17 P19 P20 P24 P25 P28 P29 : Point)
    (L00 L02 L26 : Line)
    (C22 : Circle)
    (h00 : angle_bisector_line P15 P24 P25 P03 L26)
    (h01 : directed_angle_eq_mod_pi P07 P02 P29 P24 P19 P14)
    (h02 : line_circle_intersection P03 L02 C22)
    (h03 : between P13 P28 P11)
    (h04 : angle_bisector_line P19 P20 P17 P28 L00)
    : angle_bisector P15 P24 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0494
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0494

theorem v06_sealed_holdout_0495
    (P03 P05 P06 P08 P11 P13 P14 P17 P20 P22 P24 P25 P30 P31 : Point)
    (L24 : Line)
    (h00 : angle_bisector_line P11 P25 P24 P03 L24)
    (h01 : between P11 P30 P17)
    (h02 : between P14 P11 P08)
    (h03 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    (h04 : between P20 P05 P22)
    : angle_bisector P11 P25 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0495
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0495

theorem v06_sealed_holdout_0496
    (P00 P03 P04 P06 P07 P14 P15 P16 P19 P20 P23 P24 P27 P31 : Point)
    (L04 L18 : Line)
    (C02 C10 C30 : Circle)
    (h00 : directed_angle_eq_mod_pi P20 P00 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : angle_bisector_line P06 P14 P16 P27 L04)
    (h03 : line_circle_intersection P03 L18 C10)
    (h04 : circle_circle_intersection P19 C30 C02)
    : directed_angle_eq_mod_pi P20 P00 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0496
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0496

theorem v06_sealed_holdout_0497
    (P00 P02 P03 P04 P07 P09 P10 P11 P16 P21 P22 P24 P25 P30 P31 : Point)
    (L02 : Line)
    (C06 : Circle)
    (h00 : directed_angle_eq_mod_2pi P09 P04 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : midpoint P30 P11 P24)
    (h03 : area_le P31 P10 P21 P00 P11 P22)
    (h04 : line_circle_intersection P03 L02 C06)
    : directed_angle_eq_mod_2pi P09 P04 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0497
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0497

theorem v06_sealed_holdout_0498
    (P00 P04 P06 P07 P09 P13 P15 P16 P19 P22 P23 P24 P26 P31 : Point)
    (L26 : Line)
    (C12 : Circle)
    (h00 : directed_angle_eq_mod_pi P22 P00 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : line_circle_intersection P19 L26 C12)
    (h03 : area_le P06 P19 P00 P13 P26 P07)
    (h04 : midpoint P09 P00 P23)
    : directed_angle_eq_mod_pi P22 P00 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0498
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0498

theorem v06_sealed_holdout_0499
    (P01 P02 P04 P07 P09 P10 P11 P12 P13 P14 P16 P20 P21 P25 P27 P28 P29 P30 P31 : Point)
    (h00 : directed_angle_eq_mod_2pi P11 P04 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : area_le P12 P29 P14 P31 P16 P01)
    (h03 : midpoint P13 P28 P11)
    (h04 : area_le P16 P09 P02 P27 P20 P13)
    : directed_angle_eq_mod_2pi P11 P04 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0499
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0499

theorem v06_sealed_holdout_0500
    (P00 P05 P06 P07 P08 P09 P11 P13 P14 P15 P16 P17 P18 P20 P22 P23 P24 P31 : Point)
    (C27 : Circle)
    (h00 : circle_through_three_noncollinear_points P00 P15 P16 C27)
    (h01 : between P14 P11 P08)
    (h02 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    (h03 : directed_angle_eq_mod_pi P20 P05 P22 P07 P24 P09)
    (h04 : between P23 P18 P13)
    : triangle_pred P00 P15 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0500
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0500

theorem v06_sealed_holdout_0501
    (P01 P03 P06 P07 P11 P14 P15 P16 P19 P20 P21 P26 P27 : Point)
    (L00 : Line)
    (C02 C06 C18 C26 : Circle)
    (h00 : equilateral P21 P15 P06)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : angle_bisector_line P11 P14 P16 P27 L00)
    (h03 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    (h04 : circle_circle_intersection P03 C26 C18)
    : triangle_pred P21 P15 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0501
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0501

theorem v06_sealed_holdout_0502
    (P00 P01 P02 P03 P04 P05 P12 P15 P16 P19 P23 : Point)
    (L18 : Line)
    (C02 C09 C14 : Circle)
    (h00 : circle_through_three_noncollinear_points P02 P15 P16 C09)
    (h01 : line_circle_intersection P03 L18 C02)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : midpoint P02 P23 P12)
    (h04 : area_le P05 P04 P03 P02 P01 P00)
    : triangle_pred P02 P15 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0502
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0502

theorem v06_sealed_holdout_0503
    (P00 P06 P07 P08 P09 P11 P13 P15 P16 P19 P20 P23 P26 P27 : Point)
    (L16 L28 : Line)
    (h00 : equilateral P23 P15 P06)
    (h01 : angle_bisector_line P08 P11 P16 P27 L28)
    (h02 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    (h03 : midpoint P09 P00 P23)
    (h04 : angle_bisector_line P23 P20 P16 P27 L16)
    : triangle_pred P23 P15 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0503
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0503

theorem v06_sealed_holdout_0504
    (P02 P06 P09 P10 P11 P13 P15 P16 P19 P20 P22 P24 P25 P26 P27 P28 P31 : Point)
    (h00 : equilateral P24 P15 P06)
    (h01 : midpoint P10 P15 P20)
    (h02 : directed_angle_eq_mod_pi P13 P28 P11 P26 P09 P24)
    (h03 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    (h04 : area_le P19 P22 P25 P28 P31 P02)
    : triangle_pred P24 P15 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0504
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0504

theorem v06_sealed_holdout_0505
    (P04 P05 P09 P14 P16 P19 P20 P22 P26 P31 : Point)
    (L26 : Line)
    (C02 C04 C22 : Circle)
    (RF60 : Reflection)
    (h00 : between P22 P19 P16)
    (h01 : circle_circle_intersection P19 C22 C02)
    (h02 : between P20 P05 P22)
    (h03 : line_circle_intersection P19 L26 C04)
    (h04 : area_le P26 P31 P04 P09 P14 P19)
    : reflection_image RF60 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0505
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0505

theorem v06_sealed_holdout_0506
    (P01 P07 P11 P12 P14 P15 P16 P18 P19 P20 P21 P24 P25 P26 P27 P28 P29 P30 : Point)
    (L00 L10 : Line)
    (C00 : Circle)
    (HOM17 : Homothety)
    (h00 : area_le P29 P28 P27 P26 P25 P24)
    (h01 : angle_bisector_line P11 P12 P16 P27 L00)
    (h02 : area_le P27 P14 P01 P20 P07 P26)
    (h03 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    (h04 : line_circle_intersection P19 L10 C00)
    : homothety_image HOM17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0506
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0506

theorem v06_sealed_holdout_0507
    (P00 P01 P02 P03 P04 P05 P06 P07 P08 P09 P16 P19 P20 P27 P28 : Point)
    (L00 L26 : Line)
    (C10 C18 C20 : Circle)
    (INV42 : Inversion)
    (h00 : directed_angle_eq_mod_pi P04 P05 P06 P07 P08 P09)
    (h01 : line_circle_intersection P19 L26 C20)
    (h02 : circle_circle_intersection P03 C10 C18)
    (h03 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    (h04 : angle_bisector_line P27 P20 P16 P28 L00)
    : inversion_image INV42 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0507
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0507

theorem v06_sealed_holdout_0508
    (P00 P03 P05 P09 P11 P13 P14 P16 P20 P23 P27 P28 : Point)
    (L06 L12 L24 : Line)
    (C18 C19 C24 : Circle)
    (SP07 : SpiralSimilarity)
    (h00 : line_circle_intersection P11 L06 C24)
    (h01 : angle_bisector_line P13 P11 P16 P27 L24)
    (h02 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h03 : circle_circle_intersection P03 C18 C19)
    (h04 : angle_bisector_line P28 P20 P16 P27 L12)
    : spiral_similarity_center SP07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0508
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0508

theorem v06_sealed_holdout_0509
    (P03 P08 P15 P17 P19 P23 P28 P31 : Point)
    (L02 : Line)
    (C06 C30 : Circle)
    (h00 : P17 = P08)
    (h01 : P15 = P19)
    (h02 : P28 = P31)
    (h03 : circle_circle_intersection P23 C30 C06)
    (h04 : line_circle_intersection P03 L02 C30)
    : rotation_preserves_collinear P17 P15 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0509
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0509

theorem v06_sealed_holdout_0510
    (P01 P03 P05 P07 P08 P09 P10 P12 P19 P20 P22 P24 P25 P26 P27 P29 : Point)
    (L26 : Line)
    (C04 C10 C18 C31 : Circle)
    (h00 : circle_with_center_through_point P26 P01 C31)
    (h01 : area_le P20 P05 P22 P07 P24 P09)
    (h02 : line_circle_intersection P19 L26 C04)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : area_le P29 P12 P27 P10 P25 P08)
    : on_circle P01 C31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0510
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0510

theorem v06_sealed_holdout_0511
    (P02 P04 P06 P07 P08 P14 P19 P21 P23 P24 P25 P27 P29 P30 : Point)
    (L10 L21 : Line)
    (C00 C17 : Circle)
    (h00 : line_circle_intersection P24 L21 C17)
    (h01 : between P30 P27 P24)
    (h02 : line_circle_intersection P19 L10 C00)
    (h03 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    (h04 : area_le P07 P02 P29 P24 P19 P14)
    : on_circle P24 C17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0511
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0511

theorem v06_sealed_holdout_0512
    (P00 P03 P05 P10 P17 P18 P20 P21 P22 P28 : Point)
    (L04 L18 L24 L28 : Line)
    (C10 C28 : Circle)
    (h00 : chord P21 P00 C28)
    (h01 : angle_bisector_line P22 P10 P17 P28 L04)
    (h02 : line_circle_intersection P03 L18 C10)
    (h03 : angle_bisector_line P00 P17 P18 P28 L28)
    (h04 : angle_bisector_line P05 P20 P17 P28 L24)
    : on_circle P21 C28 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0512
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0512

theorem v06_sealed_holdout_0513
    (P01 P03 P07 P17 P18 P19 P27 P28 P30 : Point)
    (L08 L18 L22 L26 : Line)
    (C02 C06 C20 C22 : Circle)
    (h00 : tangent_chord_angle P30 P07 P27 L22 C22)
    (h01 : line_circle_intersection P03 L18 C02)
    (h02 : line_circle_intersection P19 L26 C20)
    (h03 : angle_bisector_line P01 P17 P18 P28 L08)
    (h04 : circle_circle_intersection P19 C06 C02)
    : on_circle P27 C22 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0513
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0513

theorem v06_sealed_holdout_0514
    (P03 P07 P12 P16 P19 P21 P22 P25 P28 P29 P30 : Point)
    (L23 : Line)
    (C18 C20 C26 : Circle)
    (h00 : line_circle_intersection P07 L23 C20)
    (h01 : midpoint P19 P22 P25)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : area_le P25 P16 P07 P30 P21 P12)
    (h04 : midpoint P28 P29 P30)
    : on_line P07 L23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0514
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0514

theorem v06_sealed_holdout_0515
    (P00 P03 P04 P06 P08 P09 P10 P11 P12 P13 P18 P23 P25 P27 P28 P29 : Point)
    (L02 L23 : Line)
    (C22 : Circle)
    (h00 : altitude P28 P18 P13 P23 L23)
    (h01 : line_circle_intersection P03 L02 C22)
    (h02 : area_le P29 P12 P27 P10 P25 P08)
    (h03 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    (h04 : between P03 P06 P09)
    : on_line P13 L23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0515
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0515

theorem v06_sealed_holdout_0516
    (P01 P02 P03 P04 P07 P08 P12 P14 P15 P19 P22 P23 P24 P29 : Point)
    (L17 L18 : Line)
    (C18 C26 : Circle)
    (h00 : altitude P24 P19 P12 P23 L17)
    (h01 : circle_circle_intersection P03 C26 C18)
    (h02 : directed_angle_eq_mod_pi P01 P08 P15 P22 P29 P04)
    (h03 : line_circle_intersection P03 L18 C18)
    (h04 : area_le P07 P02 P29 P24 P19 P14)
    : on_line P12 L17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0516
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0516

theorem v06_sealed_holdout_0517
    (P08 P10 P11 P14 P17 P19 P27 P28 : Point)
    (L00 L04 L26 : Line)
    (C02 C12 C22 C28 : Circle)
    (h00 : line_circle_intersection P10 L04 C12)
    (h01 : angle_bisector_line P27 P10 P17 P28 L00)
    (h02 : line_circle_intersection P19 L26 C28)
    (h03 : midpoint P14 P11 P08)
    (h04 : circle_circle_intersection P19 C22 C02)
    : on_line P10 L04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0517
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0517

theorem v06_sealed_holdout_0518
    (P01 P03 P05 P06 P10 P11 P15 P16 P19 P20 P21 P23 P24 P26 P27 : Point)
    (C10 C18 : Circle)
    (h00 : equilateral P23 P11 P01)
    (h01 : directed_angle_eq_mod_pi P15 P26 P05 P16 P27 P06)
    (h02 : circle_circle_intersection P03 C10 C18)
    (h03 : midpoint P21 P20 P19)
    (h04 : midpoint P24 P01 P10)
    : equal_length P23 P11 P11 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0518
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0518

theorem v06_sealed_holdout_0519
    (P00 P03 P07 P10 P12 P16 P19 P21 P22 P23 P25 P29 P30 : Point)
    (C18 C19 : Circle)
    (h00 : equilateral P19 P12 P00)
    (h01 : between P19 P22 P25)
    (h02 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    (h03 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h04 : circle_circle_intersection P03 C18 C19)
    : equal_length P19 P12 P12 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0519
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0519

theorem v06_sealed_holdout_0520
    (P03 P06 P09 P11 P12 P15 P16 P18 P19 P21 P23 P24 P26 P30 P31 : Point)
    (C02 C06 C18 : Circle)
    (h00 : length_sum P24 P30 P31 P09 P16 P23)
    (h01 : area_le P31 P26 P21 P16 P11 P06)
    (h02 : circle_circle_intersection P19 C06 C02)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : area_le P03 P06 P09 P12 P15 P18)
    : length_sum P31 P09 P24 P30 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0520
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0520

theorem v06_sealed_holdout_0521
    (P00 P02 P03 P05 P06 P07 P08 P10 P15 P16 P20 P21 P23 P25 P26 P27 P29 P30 : Point)
    (h00 : equal_length P21 P08 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : directed_angle_eq_mod_pi P06 P03 P00 P29 P26 P23)
    (h03 : between P07 P02 P29)
    (h04 : area_le P10 P15 P20 P25 P30 P03)
    : equal_length P21 P08 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0521
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0521

theorem v06_sealed_holdout_0522
    (P02 P03 P05 P10 P12 P13 P14 P16 P18 P19 P21 P22 P23 P24 P27 : Point)
    (L20 L24 : Line)
    (C06 : Circle)
    (h00 : area_eq P10 P12 P22 P02 P13 P23)
    (h01 : area_eq P02 P13 P23 P03 P14 P24)
    (h02 : line_circle_intersection P19 L24 C06)
    (h03 : angle_bisector_line P05 P18 P16 P27 L24)
    (h04 : angle_bisector_line P10 P21 P16 P27 L20)
    : area_eq P10 P12 P22 P03 P14 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0522
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0522

theorem v06_sealed_holdout_0523
    (P03 P05 P08 P15 P16 P19 P20 P21 P23 P27 P31 : Point)
    (L18 : Line)
    (C10 C14 C15 : Circle)
    (h00 : equal_length P23 P08 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : circle_circle_intersection P31 C14 C15)
    (h03 : between P21 P20 P19)
    (h04 : line_circle_intersection P03 L18 C10)
    : equal_length P23 P08 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0523
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0523

theorem v06_sealed_holdout_0524
    (P02 P03 P10 P11 P12 P13 P17 P21 P23 P25 P26 P28 P31 : Point)
    (L18 L20 L28 : Line)
    (C02 : Circle)
    (h00 : angle_bisector_line P13 P25 P26 P03 L28)
    (h01 : angle_bisector_line P02 P11 P17 P28 L20)
    (h02 : line_circle_intersection P03 L18 C02)
    (h03 : midpoint P31 P10 P21)
    (h04 : midpoint P02 P23 P12)
    : angle_bisector P13 P25 P26 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0524
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0524

theorem v06_sealed_holdout_0525
    (P00 P03 P06 P09 P12 P18 P24 P25 P26 P27 P29 : Point)
    (L26 : Line)
    (C18 C26 : Circle)
    (h00 : angle_bisector_line P09 P26 P24 P03 L26)
    (h01 : midpoint P29 P12 P27)
    (h02 : midpoint P00 P25 P18)
    (h03 : midpoint P03 P06 P09)
    (h04 : circle_circle_intersection P03 C26 C18)
    : angle_bisector P09 P26 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0525
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0525

theorem v06_sealed_holdout_0526
    (P01 P02 P04 P07 P10 P11 P13 P14 P15 P16 P18 P19 P20 P23 P24 P28 P29 P31 : Point)
    (h00 : directed_angle_eq_mod_pi P18 P01 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : area_le P07 P02 P29 P24 P19 P14)
    (h03 : between P10 P15 P20)
    (h04 : midpoint P13 P28 P11)
    : directed_angle_eq_mod_pi P18 P01 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0526
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0526

theorem v06_sealed_holdout_0527
    (P02 P03 P05 P07 P08 P10 P11 P16 P19 P20 P21 P25 P29 P30 : Point)
    (C02 C18 C19 C22 : Circle)
    (h00 : directed_angle_eq_mod_2pi P07 P05 P10 P21 P30 P08)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P08 P16 P25 P02)
    (h02 : area_le P16 P25 P02 P11 P20 P29)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : circle_circle_intersection P03 C18 C19)
    : directed_angle_eq_mod_2pi P07 P05 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0527
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0527

theorem v06_sealed_holdout_0528
    (P01 P04 P05 P07 P10 P14 P15 P16 P17 P18 P19 P20 P21 P23 P24 P27 P28 P31 : Point)
    (h00 : directed_angle_eq_mod_pi P20 P01 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : area_le P21 P20 P19 P18 P17 P16)
    (h03 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    (h04 : midpoint P27 P14 P01)
    : directed_angle_eq_mod_pi P20 P01 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0528
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0528

theorem v06_sealed_holdout_0529
    (P01 P02 P05 P07 P09 P10 P11 P12 P16 P21 P22 P23 P25 P30 P31 : Point)
    (L01 : Line)
    (C29 : Circle)
    (h00 : directed_angle_eq_mod_2pi P09 P05 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : line_circle_intersection P07 L01 C29)
    (h03 : between P31 P10 P21)
    (h04 : directed_angle_eq_mod_pi P02 P23 P12 P01 P22 P11)
    : directed_angle_eq_mod_2pi P09 P05 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0529
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0529

theorem v06_sealed_holdout_0530
    (P00 P03 P04 P06 P09 P11 P12 P15 P16 P17 P18 P21 P25 P27 P29 P30 : Point)
    (L20 : Line)
    (C13 C18 C26 : Circle)
    (h00 : circle_through_three_noncollinear_points P30 P16 P17 C13)
    (h01 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    (h02 : area_le P03 P06 P09 P12 P15 P18)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : angle_bisector_line P18 P21 P16 P27 L20)
    : triangle_pred P30 P16 P17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0530
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0530

theorem v06_sealed_holdout_0531
    (P02 P04 P06 P09 P12 P13 P15 P16 P19 P20 P27 : Point)
    (L08 L10 L12 : Line)
    (C08 : Circle)
    (h00 : equilateral P19 P16 P06)
    (h01 : angle_bisector_line P04 P12 P16 P27 L12)
    (h02 : angle_bisector_line P09 P15 P16 P27 L08)
    (h03 : line_circle_intersection P19 L10 C08)
    (h04 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    : triangle_pred P19 P16 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0531
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0531

theorem v06_sealed_holdout_0532
    (P00 P02 P05 P06 P08 P11 P13 P14 P15 P16 P17 P18 P20 P23 P24 P27 P31 : Point)
    (L16 : Line)
    (C27 : Circle)
    (h00 : circle_through_three_noncollinear_points P00 P16 P17 C27)
    (h01 : directed_angle_eq_mod_pi P14 P11 P08 P05 P02 P31)
    (h02 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    (h03 : angle_bisector_line P15 P18 P16 P27 L16)
    (h04 : midpoint P23 P18 P13)
    : triangle_pred P00 P16 P17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0532
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0532

theorem v06_sealed_holdout_0533
    (P01 P03 P06 P12 P14 P16 P21 P24 P27 P30 : Point)
    (L04 : Line)
    (C02 C18 : Circle)
    (h00 : equilateral P21 P16 P06)
    (h01 : angle_bisector_line P06 P12 P16 P27 L04)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : between P27 P14 P01)
    (h04 : midpoint P30 P27 P24)
    : triangle_pred P21 P16 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0533
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0533

theorem v06_sealed_holdout_0534
    (P00 P01 P02 P03 P04 P05 P06 P07 P10 P11 P12 P16 P21 P22 P23 P27 P31 : Point)
    (L16 : Line)
    (h00 : equilateral P22 P16 P06)
    (h01 : angle_bisector_line P07 P12 P16 P27 L16)
    (h02 : midpoint P31 P10 P21)
    (h03 : area_le P02 P23 P12 P01 P22 P11)
    (h04 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    : triangle_pred P22 P16 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0534
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0534

theorem v06_sealed_holdout_0535
    (P00 P01 P03 P05 P08 P09 P12 P16 P19 P21 P23 P26 P27 : Point)
    (L16 L28 : Line)
    (C18 C26 : Circle)
    (RF14 : Reflection)
    (h00 : directed_angle_eq_mod_pi P08 P01 P26 P19 P12 P05)
    (h01 : angle_bisector_line P08 P12 P16 P27 L28)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : between P09 P00 P23)
    (h04 : angle_bisector_line P23 P21 P16 P27 L16)
    : reflection_image RF14 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0535
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0535

theorem v06_sealed_holdout_0536
    (P03 P10 P11 P13 P15 P19 P20 P25 P27 P28 P30 : Point)
    (L10 L18 : Line)
    (C02 C20 C26 C30 : Circle)
    (HOM31 : Homothety)
    (h00 : line_circle_intersection P27 L10 C20)
    (h01 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    (h02 : midpoint P13 P28 P11)
    (h03 : line_circle_intersection P03 L18 C26)
    (h04 : circle_circle_intersection P19 C30 C02)
    : homothety_image HOM31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0536
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0536

theorem v06_sealed_holdout_0537
    (P04 P07 P13 P15 P16 P17 P18 P23 P24 P26 P27 P31 : Point)
    (L16 : Line)
    (C22 C30 : Circle)
    (INV52 : Inversion)
    (h00 : circle_circle_intersection P07 C30 C22)
    (h01 : between P17 P24 P31)
    (h02 : angle_bisector_line P15 P16 P17 P27 L16)
    (h03 : between P23 P18 P13)
    (h04 : midpoint P26 P31 P04)
    : inversion_image INV52 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0537
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0537

theorem v06_sealed_holdout_0538
    (P01 P06 P11 P12 P13 P14 P16 P19 P22 P24 P27 P30 P31 : Point)
    (L00 L04 : Line)
    (C02 C22 : Circle)
    (SP13 : SpiralSimilarity)
    (h00 : angle_bisector_line P06 P22 P31 P13 L04)
    (h01 : angle_bisector_line P11 P12 P16 P27 L00)
    (h02 : midpoint P27 P14 P01)
    (h03 : between P30 P27 P24)
    (h04 : circle_circle_intersection P19 C22 C02)
    : spiral_similarity_center SP13 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0538
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0538

theorem v06_sealed_holdout_0539
    (P04 P05 P06 P08 P15 P16 P19 P21 P27 P28 P31 : Point)
    (L00 : Line)
    (h00 : P15 = P08)
    (h01 : P16 = P19)
    (h02 : P28 = P31)
    (h03 : midpoint P04 P05 P06)
    (h04 : angle_bisector_line P27 P21 P16 P28 L00)
    : rotation_preserves_collinear P15 P16 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0539
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0539

theorem v06_sealed_holdout_0540
    (P00 P02 P05 P09 P12 P13 P14 P16 P18 P19 P23 P24 P27 P28 : Point)
    (L16 L24 : Line)
    (C02 C03 C14 : Circle)
    (h00 : circle_with_center_through_point P24 P02 C03)
    (h01 : angle_bisector_line P13 P12 P16 P27 L24)
    (h02 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h03 : angle_bisector_line P23 P18 P16 P27 L16)
    (h04 : circle_circle_intersection P19 C14 C02)
    : on_circle P02 C03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0540
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0540

theorem v06_sealed_holdout_0541
    (P02 P03 P07 P11 P16 P17 P19 P22 P25 P28 P31 : Point)
    (L00 L21 : Line)
    (C31 : Circle)
    (h00 : line_circle_intersection P22 L21 C31)
    (h01 : angle_bisector_line P19 P11 P17 P28 L00)
    (h02 : area_le P19 P22 P25 P28 P31 P02)
    (h03 : between P22 P03 P16)
    (h04 : between P25 P16 P07)
    : on_circle P22 C31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0541
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0541

theorem v06_sealed_holdout_0542
    (P00 P01 P04 P09 P11 P14 P17 P18 P19 P20 P25 P26 P28 P29 P31 : Point)
    (L12 : Line)
    (C02 C04 C06 : Circle)
    (h00 : chord P19 P01 C04)
    (h01 : angle_bisector_line P20 P11 P17 P28 L12)
    (h02 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : area_le P00 P25 P18 P11 P04 P29)
    : on_circle P19 C04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0542
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0542

theorem v06_sealed_holdout_0543
    (P03 P08 P19 P24 P27 P28 P30 : Point)
    (L02 L10 L26 : Line)
    (C00 C04 C18 C19 C26 : Circle)
    (h00 : tangent_chord_angle P28 P08 P27 L02 C26)
    (h01 : midpoint P30 P27 P24)
    (h02 : line_circle_intersection P19 L10 C00)
    (h03 : circle_circle_intersection P03 C18 C19)
    (h04 : line_circle_intersection P19 L26 C04)
    : on_circle P27 C26 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0543
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0543

theorem v06_sealed_holdout_0544
    (P02 P03 P04 P05 P08 P11 P14 P19 P31 : Point)
    (L18 L25 : Line)
    (C02 C04 C10 C30 : Circle)
    (h00 : line_circle_intersection P05 L25 C04)
    (h01 : midpoint P05 P04 P03)
    (h02 : line_circle_intersection P03 L18 C10)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : directed_angle_eq_mod_pi P14 P11 P08 P05 P02 P31)
    : on_line P05 L25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0544
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0544

theorem v06_sealed_holdout_0545
    (P05 P06 P07 P11 P13 P15 P16 P17 P18 P19 P20 P21 P23 P26 P27 P28 : Point)
    (L16 L29 : Line)
    (h00 : altitude P26 P19 P13 P23 L29)
    (h01 : angle_bisector_line P23 P11 P17 P28 L16)
    (h02 : directed_angle_eq_mod_pi P15 P26 P05 P16 P27 P06)
    (h03 : directed_angle_eq_mod_pi P18 P07 P28 P17 P06 P27)
    (h04 : midpoint P21 P20 P19)
    : on_line P13 L29 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0545
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0545

theorem v06_sealed_holdout_0546
    (P03 P07 P12 P16 P19 P20 P21 P22 P23 P25 P27 P30 : Point)
    (L00 L23 : Line)
    (h00 : altitude P22 P20 P12 P23 L23)
    (h01 : angle_bisector_line P19 P12 P16 P27 L00)
    (h02 : between P19 P22 P25)
    (h03 : between P22 P03 P16)
    (h04 : area_le P25 P16 P07 P30 P21 P12)
    : on_line P12 L23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0546
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0546

theorem v06_sealed_holdout_0547
    (P03 P04 P08 P09 P12 P14 P17 P18 P19 P26 P27 P28 P29 P31 : Point)
    (L00 L06 : Line)
    (C02 C28 C30 : Circle)
    (h00 : line_circle_intersection P08 L06 C28)
    (h01 : area_le P26 P31 P04 P09 P14 P19)
    (h02 : midpoint P29 P12 P27)
    (h03 : angle_bisector_line P03 P18 P17 P28 L00)
    (h04 : circle_circle_intersection P19 C30 C02)
    : on_line P08 L06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0547
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0547

theorem v06_sealed_holdout_0548
    (P01 P02 P04 P06 P07 P08 P10 P12 P15 P20 P21 P23 P25 P29 : Point)
    (h00 : equilateral P21 P12 P01)
    (h01 : midpoint P01 P08 P15)
    (h02 : area_le P04 P21 P06 P23 P08 P25)
    (h03 : between P07 P02 P29)
    (h04 : between P10 P15 P20)
    : equal_length P21 P12 P12 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0548
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0548

theorem v06_sealed_holdout_0549
    (P00 P02 P03 P05 P08 P11 P12 P13 P14 P17 P19 P21 P26 P31 : Point)
    (L10 L26 : Line)
    (C24 C28 : Circle)
    (h00 : equilateral P17 P13 P00)
    (h01 : line_circle_intersection P19 L10 C24)
    (h02 : area_le P08 P17 P26 P03 P12 P21)
    (h03 : line_circle_intersection P19 L26 C28)
    (h04 : directed_angle_eq_mod_pi P14 P11 P08 P05 P02 P31)
    : equal_length P17 P13 P13 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0549
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0549

theorem v06_sealed_holdout_0550
    (P03 P07 P09 P16 P18 P19 P20 P21 P22 P23 P28 P30 P31 : Point)
    (L28 : Line)
    (C02 C14 : Circle)
    (h00 : length_sum P22 P31 P30 P09 P16 P23)
    (h01 : line_circle_intersection P03 L28 C02)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : between P18 P07 P28)
    (h04 : between P21 P20 P19)
    : length_sum P30 P09 P22 P31 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0550
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0550

theorem v06_sealed_holdout_0551
    (P02 P03 P05 P09 P15 P16 P19 P27 : Point)
    (L20 : Line)
    (C14 C18 C19 C30 : Circle)
    (h00 : equal_length P19 P09 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : circle_circle_intersection P15 C14 C30)
    (h03 : angle_bisector_line P02 P19 P16 P27 L20)
    (h04 : circle_circle_intersection P03 C18 C19)
    : equal_length P19 P09 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0551
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0551

theorem v06_sealed_holdout_0552
    (P00 P02 P03 P04 P06 P08 P09 P11 P12 P13 P14 P18 P20 P22 P23 P24 P25 P29 P31 : Point)
    (L20 : Line)
    (h00 : area_eq P08 P13 P22 P02 P12 P23)
    (h01 : area_eq P02 P12 P23 P03 P14 P24)
    (h02 : angle_bisector_line P20 P22 P31 P13 L20)
    (h03 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    (h04 : midpoint P03 P06 P09)
    : area_eq P08 P13 P22 P03 P14 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0552
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0552

theorem v06_sealed_holdout_0553
    (P00 P03 P04 P05 P06 P09 P15 P16 P19 P21 P27 : Point)
    (L12 : Line)
    (C10 C18 : Circle)
    (h00 : equal_length P21 P09 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : midpoint P06 P03 P00)
    (h03 : angle_bisector_line P04 P19 P16 P27 L12)
    (h04 : circle_circle_intersection P03 C10 C18)
    : equal_length P21 P09 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0553
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0553

theorem v06_sealed_holdout_0554
    (P03 P04 P10 P11 P17 P23 P24 P25 P26 P30 P31 : Point)
    (L02 L30 : Line)
    (C14 C18 C19 : Circle)
    (h00 : angle_bisector_line P11 P26 P25 P03 L30)
    (h01 : area_le P11 P30 P17 P04 P23 P10)
    (h02 : line_circle_intersection P03 L02 C14)
    (h03 : midpoint P17 P24 P31)
    (h04 : circle_circle_intersection P03 C18 C19)
    : angle_bisector P11 P26 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0554
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0554

theorem v06_sealed_holdout_0555
    (P01 P03 P05 P06 P07 P10 P15 P17 P18 P19 P20 P21 P24 P26 P27 P28 : Point)
    (L28 : Line)
    (h00 : angle_bisector_line P07 P27 P24 P03 L28)
    (h01 : midpoint P15 P26 P05)
    (h02 : area_le P18 P07 P28 P17 P06 P27)
    (h03 : midpoint P21 P20 P19)
    (h04 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    : angle_bisector P07 P27 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0555
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0555

theorem v06_sealed_holdout_0556
    (P02 P03 P04 P07 P10 P15 P16 P17 P19 P21 P23 P24 P31 : Point)
    (L10 L18 : Line)
    (C02 C16 : Circle)
    (h00 : directed_angle_eq_mod_pi P16 P02 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P17 P24)
    (h02 : line_circle_intersection P19 L10 C16)
    (h03 : line_circle_intersection P03 L18 C02)
    (h04 : midpoint P31 P10 P21)
    : directed_angle_eq_mod_pi P16 P02 P04 P07 P17 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0556
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0556

theorem v06_sealed_holdout_0557
    (P02 P03 P05 P06 P07 P09 P10 P13 P16 P21 P22 P23 P25 P27 P30 : Point)
    (L05 L24 : Line)
    (C25 : Circle)
    (h00 : directed_angle_eq_mod_2pi P05 P06 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : line_circle_intersection P23 L05 C25)
    (h03 : midpoint P03 P06 P09)
    (h04 : angle_bisector_line P13 P22 P16 P27 L24)
    : directed_angle_eq_mod_2pi P05 P06 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0557
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0557

theorem v06_sealed_holdout_0558
    (P02 P04 P07 P10 P11 P13 P15 P16 P17 P18 P20 P23 P24 P27 P28 P31 : Point)
    (L12 : Line)
    (h00 : directed_angle_eq_mod_pi P18 P02 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : angle_bisector_line P04 P16 P17 P27 L12)
    (h03 : midpoint P10 P15 P20)
    (h04 : midpoint P13 P28 P11)
    : directed_angle_eq_mod_pi P18 P02 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0558
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0558

theorem v06_sealed_holdout_0559
    (P02 P05 P06 P07 P08 P09 P10 P13 P16 P19 P20 P21 P22 P23 P24 P25 P27 P30 P31 : Point)
    (L10 L12 : Line)
    (C00 : Circle)
    (h00 : directed_angle_eq_mod_2pi P07 P06 P10 P21 P30 P08)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P08 P16 P25 P02)
    (h02 : angle_bisector_line P27 P23 P31 P13 L12)
    (h03 : line_circle_intersection P19 L10 C00)
    (h04 : directed_angle_eq_mod_pi P20 P05 P22 P07 P24 P09)
    : directed_angle_eq_mod_2pi P07 P06 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0559
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0559

theorem v06_sealed_holdout_0560
    (P01 P03 P05 P06 P10 P14 P16 P17 P19 P24 P27 P28 : Point)
    (L04 : Line)
    (C10 C18 C31 : Circle)
    (h00 : circle_through_three_noncollinear_points P28 P17 P16 C31)
    (h01 : circle_circle_intersection P03 C10 C18)
    (h02 : angle_bisector_line P06 P16 P17 P27 L04)
    (h03 : area_le P24 P01 P10 P19 P28 P05)
    (h04 : between P27 P14 P01)
    : triangle_pred P28 P17 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0560
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0560

theorem v06_sealed_holdout_0561
    (P02 P03 P06 P12 P17 P18 P19 P23 : Point)
    (L18 L26 : Line)
    (C02 C20 C22 : Circle)
    (h00 : equilateral P17 P18 P06)
    (h01 : circle_circle_intersection P19 C22 C02)
    (h02 : line_circle_intersection P03 L18 C02)
    (h03 : line_circle_intersection P19 L26 C20)
    (h04 : midpoint P02 P23 P12)
    : triangle_pred P17 P18 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0561
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0561

theorem v06_sealed_holdout_0562
    (P00 P03 P06 P09 P13 P16 P17 P19 P23 P27 P30 : Point)
    (L18 L24 : Line)
    (C13 C26 : Circle)
    (h00 : circle_through_three_noncollinear_points P30 P17 P16 C13)
    (h01 : line_circle_intersection P03 L18 C26)
    (h02 : midpoint P03 P06 P09)
    (h03 : angle_bisector_line P13 P19 P16 P27 L24)
    (h04 : midpoint P09 P00 P23)
    : triangle_pred P30 P17 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0562
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0562

theorem v06_sealed_holdout_0563
    (P03 P04 P06 P10 P11 P13 P15 P16 P17 P19 P20 P27 P28 : Point)
    (L12 L18 : Line)
    (C26 : Circle)
    (h00 : equilateral P19 P17 P06)
    (h01 : angle_bisector_line P04 P13 P16 P27 L12)
    (h02 : between P10 P15 P20)
    (h03 : between P13 P28 P11)
    (h04 : line_circle_intersection P03 L18 C26)
    : triangle_pred P19 P17 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0563
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0563

theorem v06_sealed_holdout_0564
    (P03 P06 P08 P11 P13 P14 P15 P16 P17 P18 P19 P20 P23 P27 P30 : Point)
    (L10 L16 : Line)
    (C00 : Circle)
    (h00 : equilateral P20 P17 P06)
    (h01 : between P14 P11 P08)
    (h02 : line_circle_intersection P19 L10 C00)
    (h03 : angle_bisector_line P15 P19 P16 P27 L16)
    (h04 : area_le P23 P18 P13 P08 P03 P30)
    : triangle_pred P20 P17 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0564
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0564

theorem v06_sealed_holdout_0565
    (P01 P05 P07 P10 P14 P15 P16 P17 P18 P19 P20 P21 P23 P24 P26 P27 P28 P30 : Point)
    (C06 C30 : Circle)
    (RF32 : Reflection)
    (h00 : circle_circle_intersection P23 C30 C06)
    (h01 : area_le P21 P20 P19 P18 P17 P16)
    (h02 : area_le P24 P01 P10 P19 P28 P05)
    (h03 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    (h04 : area_le P30 P27 P24 P21 P18 P15)
    : reflection_image RF32 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0565
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0565

theorem v06_sealed_holdout_0566
    (P00 P01 P02 P03 P04 P05 P10 P11 P12 P13 P21 P22 P23 P28 P29 P30 P31 : Point)
    (L04 : Line)
    (HOM45 : Homothety)
    (h00 : angle_bisector_line P02 P23 P31 P13 L04)
    (h01 : area_le P28 P29 P30 P31 P00 P01)
    (h02 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    (h03 : area_le P02 P23 P12 P01 P22 P11)
    (h04 : between P05 P04 P03)
    : homothety_image HOM45 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0566
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0566

theorem v06_sealed_holdout_0567
    (P00 P01 P03 P08 P09 P13 P16 P23 P26 P27 : Point)
    (L28 : Line)
    (C18 C19 C26 : Circle)
    (INV62 : Inversion)
    (h00 : midpoint P08 P01 P26)
    (h01 : angle_bisector_line P08 P13 P16 P27 L28)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : between P09 P00 P23)
    (h04 : circle_circle_intersection P03 C18 C19)
    : inversion_image INV62 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0567
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0567

theorem v06_sealed_holdout_0568
    (P02 P05 P09 P10 P13 P15 P16 P19 P27 : Point)
    (L08 L10 L26 : Line)
    (C08 C12 : Circle)
    (SP19 : SpiralSimilarity)
    (h00 : between P15 P10 P05)
    (h01 : angle_bisector_line P09 P13 P16 P27 L08)
    (h02 : line_circle_intersection P19 L10 C08)
    (h03 : between P16 P09 P02)
    (h04 : line_circle_intersection P19 L26 C12)
    : spiral_similarity_center SP19 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0568
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0568

theorem v06_sealed_holdout_0569
    (P04 P07 P08 P10 P13 P16 P17 P19 P22 P26 P28 P31 : Point)
    (h00 : P13 = P08)
    (h01 : P17 = P19)
    (h02 : P28 = P31)
    (h03 : area_le P22 P19 P16 P13 P10 P07)
    (h04 : between P26 P31 P04)
    : rotation_preserves_collinear P13 P17 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0569
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0569

theorem v06_sealed_holdout_0570
    (P01 P03 P05 P08 P10 P15 P19 P22 P24 P27 P28 P30 : Point)
    (C02 C07 C30 : Circle)
    (h00 : circle_with_center_through_point P22 P03 C07)
    (h01 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : midpoint P30 P27 P24)
    (h04 : midpoint P01 P08 P15)
    : on_circle P03 C07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0570
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0570

theorem v06_sealed_holdout_0571
    (P02 P03 P11 P12 P17 P19 P20 P23 P30 : Point)
    (L10 L21 : Line)
    (C02 C13 C18 C24 : Circle)
    (h00 : line_circle_intersection P20 L21 C13)
    (h01 : midpoint P02 P23 P12)
    (h02 : line_circle_intersection P19 L10 C24)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : between P11 P30 P17)
    : on_circle P20 C13 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0571
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0571

theorem v06_sealed_holdout_0572
    (P02 P03 P05 P15 P17 P19 P23 P26 P28 : Point)
    (L02 L10 L16 : Line)
    (C06 C12 C16 : Circle)
    (h00 : chord P17 P02 C12)
    (h01 : line_circle_intersection P19 L10 C16)
    (h02 : angle_bisector_line P23 P15 P17 P28 L16)
    (h03 : midpoint P15 P26 P05)
    (h04 : line_circle_intersection P03 L02 C06)
    : on_circle P17 C12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0572
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0572

theorem v06_sealed_holdout_0573
    (P03 P07 P09 P16 P17 P19 P22 P25 P26 P27 P28 P29 : Point)
    (L14 L24 : Line)
    (C02 C18 C30 : Circle)
    (h00 : tangent_chord_angle P26 P09 P27 L14 C30)
    (h01 : circle_circle_intersection P03 C02 C18)
    (h02 : midpoint P19 P22 P25)
    (h03 : angle_bisector_line P29 P19 P17 P28 L24)
    (h04 : midpoint P25 P16 P07)
    : on_circle P27 C30 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0573
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0573

theorem v06_sealed_holdout_0574
    (P03 P08 P13 P15 P17 P18 P19 P23 P25 P28 P30 : Point)
    (L08 L18 L27 : Line)
    (C02 C06 C20 C26 : Circle)
    (h00 : line_circle_intersection P03 L27 C20)
    (h01 : area_le P23 P18 P13 P08 P03 P30)
    (h02 : angle_bisector_line P25 P15 P17 P28 L08)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : line_circle_intersection P03 L18 C26)
    : on_line P03 L27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0574
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0574

theorem v06_sealed_holdout_0575
    (P01 P03 P08 P13 P15 P19 P20 P23 P24 : Point)
    (L03 L18 L26 : Line)
    (C04 C18 C26 : Circle)
    (h00 : altitude P24 P20 P13 P23 L03)
    (h01 : circle_circle_intersection P03 C26 C18)
    (h02 : between P01 P08 P15)
    (h03 : line_circle_intersection P03 L18 C18)
    (h04 : line_circle_intersection P19 L26 C04)
    : on_line P13 L03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0575
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0575

theorem v06_sealed_holdout_0576
    (P00 P03 P12 P13 P16 P17 P20 P21 P22 P23 P27 : Point)
    (L04 L08 L18 L28 L29 : Line)
    (C10 : Circle)
    (h00 : altitude P20 P21 P12 P23 L29)
    (h01 : angle_bisector_line P17 P13 P16 P27 L08)
    (h02 : angle_bisector_line P22 P16 P17 P27 L04)
    (h03 : line_circle_intersection P03 L18 C10)
    (h04 : angle_bisector_line P00 P23 P16 P27 L28)
    : on_line P12 L29 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0576
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0576

theorem v06_sealed_holdout_0577
    (P05 P06 P07 P12 P15 P16 P17 P18 P22 P23 P26 P27 P28 : Point)
    (L04 L08 L16 : Line)
    (C12 : Circle)
    (h00 : line_circle_intersection P06 L08 C12)
    (h01 : angle_bisector_line P23 P12 P17 P28 L16)
    (h02 : directed_angle_eq_mod_pi P15 P26 P05 P16 P27 P06)
    (h03 : midpoint P18 P07 P28)
    (h04 : angle_bisector_line P06 P22 P17 P28 L04)
    : on_line P06 L08 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0577
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0577

theorem v06_sealed_holdout_0578
    (P01 P02 P03 P07 P12 P13 P16 P17 P19 P21 P22 P25 P28 P30 P31 : Point)
    (L16 : Line)
    (C18 C26 : Circle)
    (h00 : equilateral P19 P13 P01)
    (h01 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : area_le P25 P16 P07 P30 P21 P12)
    (h04 : angle_bisector_line P07 P22 P17 P28 L16)
    : equal_length P19 P13 P13 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0578
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0578

theorem v06_sealed_holdout_0579
    (P00 P03 P04 P08 P10 P12 P13 P14 P15 P18 P23 P25 P26 P27 P29 P30 P31 : Point)
    (C02 C18 : Circle)
    (h00 : equilateral P15 P14 P00)
    (h01 : area_le P23 P18 P13 P08 P03 P30)
    (h02 : between P26 P31 P04)
    (h03 : area_le P29 P12 P27 P10 P25 P08)
    (h04 : circle_circle_intersection P03 C02 C18)
    : equal_length P15 P14 P14 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0579
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0579

theorem v06_sealed_holdout_0580
    (P00 P04 P06 P09 P13 P16 P17 P19 P20 P21 P23 P26 P27 P30 P31 : Point)
    (L20 : Line)
    (C02 C14 : Circle)
    (h00 : length_sum P20 P00 P30 P09 P16 P23)
    (h01 : angle_bisector_line P16 P23 P31 P13 L20)
    (h02 : angle_bisector_line P26 P16 P17 P27 L20)
    (h03 : midpoint P04 P21 P06)
    (h04 : circle_circle_intersection P19 C14 C02)
    : length_sum P30 P09 P20 P00 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0580
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0580

theorem v06_sealed_holdout_0581
    (P04 P05 P08 P10 P11 P14 P15 P16 P17 P20 P23 P27 P30 P31 : Point)
    (h00 : equal_length P17 P10 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : midpoint P10 P31 P20)
    (h03 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h04 : midpoint P14 P11 P08)
    : equal_length P17 P10 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0581
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0581

theorem v06_sealed_holdout_0582
    (P02 P03 P06 P07 P08 P12 P13 P14 P17 P18 P19 P20 P21 P22 P23 P24 P28 P31 : Point)
    (h00 : area_eq P06 P14 P22 P02 P12 P23)
    (h01 : area_eq P02 P12 P23 P03 P13 P24)
    (h02 : between P17 P08 P31)
    (h03 : between P18 P07 P28)
    (h04 : between P21 P20 P19)
    : area_eq P06 P14 P22 P03 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0582
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0582

theorem v06_sealed_holdout_0583
    (P00 P01 P03 P05 P07 P10 P12 P15 P16 P17 P19 P21 P24 P25 P27 P28 P29 P30 P31 : Point)
    (h00 : equal_length P19 P10 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : area_le P24 P17 P10 P03 P28 P21)
    (h03 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h04 : area_le P28 P29 P30 P31 P00 P01)
    : equal_length P19 P10 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0583
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0583

theorem v06_sealed_holdout_0584
    (P00 P03 P06 P08 P09 P10 P12 P15 P18 P19 P25 P27 P29 : Point)
    (L00 : Line)
    (C02 C18 : Circle)
    (h00 : angle_bisector_line P09 P27 P25 P03 L00)
    (h01 : area_le P29 P12 P27 P10 P25 P08)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : directed_angle_eq_mod_pi P03 P06 P09 P12 P15 P18)
    (h04 : midpoint P06 P19 P00)
    : angle_bisector P09 P27 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0584
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0584

theorem v06_sealed_holdout_0585
    (P02 P03 P05 P07 P10 P15 P19 P20 P24 P25 P28 P29 P30 : Point)
    (L10 L18 L30 : Line)
    (C00 C18 : Circle)
    (h00 : angle_bisector_line P05 P28 P24 P03 L30)
    (h01 : line_circle_intersection P19 L10 C00)
    (h02 : line_circle_intersection P03 L18 C18)
    (h03 : midpoint P07 P02 P29)
    (h04 : area_le P10 P15 P20 P25 P30 P03)
    : angle_bisector P05 P28 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0585
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0585

theorem v06_sealed_holdout_0586
    (P03 P04 P06 P07 P08 P10 P11 P13 P14 P15 P16 P17 P20 P23 P24 P30 P31 : Point)
    (h00 : directed_angle_eq_mod_pi P14 P03 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : area_le P11 P30 P17 P04 P23 P10)
    (h03 : between P14 P11 P08)
    (h04 : area_le P17 P24 P31 P06 P13 P20)
    : directed_angle_eq_mod_pi P14 P03 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0586
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0586

theorem v06_sealed_holdout_0587
    (P01 P02 P03 P07 P08 P10 P13 P16 P17 P18 P19 P20 P21 P23 P24 P25 P30 P31 : Point)
    (L12 : Line)
    (h00 : directed_angle_eq_mod_2pi P03 P07 P10 P21 P30 P08)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P08 P16 P25 P02)
    (h02 : angle_bisector_line P23 P24 P31 P13 L12)
    (h03 : area_le P21 P20 P19 P18 P17 P16)
    (h04 : between P24 P01 P10)
    : directed_angle_eq_mod_2pi P03 P07 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0587
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0587

theorem v06_sealed_holdout_0588
    (P00 P01 P03 P04 P07 P15 P16 P17 P19 P23 P24 P25 P28 P29 P30 P31 : Point)
    (L26 : Line)
    (C20 : Circle)
    (h00 : directed_angle_eq_mod_pi P16 P03 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P17 P24)
    (h02 : midpoint P25 P16 P07)
    (h03 : area_le P28 P29 P30 P31 P00 P01)
    (h04 : line_circle_intersection P19 L26 C20)
    : directed_angle_eq_mod_pi P16 P03 P04 P07 P17 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0588
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0588

theorem v06_sealed_holdout_0589
    (P02 P03 P05 P06 P07 P08 P09 P10 P12 P16 P21 P25 P30 : Point)
    (C18 C26 : Circle)
    (h00 : directed_angle_eq_mod_2pi P05 P07 P10 P21 P30 P08)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P08 P16 P25 P02)
    (h02 : between P02 P07 P12)
    (h03 : midpoint P03 P06 P09)
    (h04 : circle_circle_intersection P03 C26 C18)
    : directed_angle_eq_mod_2pi P05 P07 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0589
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0589

theorem v06_sealed_holdout_0590
    (P02 P04 P06 P07 P10 P11 P13 P14 P15 P16 P18 P19 P20 P21 P24 P26 P28 P29 : Point)
    (C17 : Circle)
    (h00 : circle_through_three_noncollinear_points P26 P18 P16 C17)
    (h01 : midpoint P04 P21 P06)
    (h02 : area_le P07 P02 P29 P24 P19 P14)
    (h03 : between P10 P15 P20)
    (h04 : midpoint P13 P28 P11)
    : triangle_pred P26 P18 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0590
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0590

theorem v06_sealed_holdout_0591
    (P05 P06 P07 P09 P15 P16 P17 P18 P19 P20 P22 P24 P27 P31 : Point)
    (L24 L26 : Line)
    (C28 : Circle)
    (h00 : equilateral P15 P18 P06)
    (h01 : line_circle_intersection P19 L26 C28)
    (h02 : angle_bisector_line P05 P17 P16 P27 L24)
    (h03 : midpoint P17 P24 P31)
    (h04 : directed_angle_eq_mod_pi P20 P05 P22 P07 P24 P09)
    : triangle_pred P15 P18 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0591
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0591

theorem v06_sealed_holdout_0592
    (P01 P03 P06 P10 P14 P16 P17 P18 P24 P27 P28 : Point)
    (L02 L04 : Line)
    (C06 C31 : Circle)
    (h00 : circle_through_three_noncollinear_points P28 P18 P16 C31)
    (h01 : line_circle_intersection P03 L02 C06)
    (h02 : angle_bisector_line P06 P17 P16 P27 L04)
    (h03 : midpoint P24 P01 P10)
    (h04 : between P27 P14 P01)
    : triangle_pred P28 P18 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0592
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0592

theorem v06_sealed_holdout_0593
    (P00 P01 P02 P03 P04 P05 P07 P10 P11 P12 P17 P21 P22 P23 P31 : Point)
    (C18 C19 : Circle)
    (h00 : equilateral P22 P17 P07)
    (h01 : circle_circle_intersection P03 C18 C19)
    (h02 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    (h03 : midpoint P02 P23 P12)
    (h04 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    : triangle_pred P22 P17 P07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0593
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0593

theorem v06_sealed_holdout_0594
    (P03 P06 P08 P13 P16 P17 P18 P19 P20 P23 P27 : Point)
    (L20 L24 L28 : Line)
    (C02 C18 : Circle)
    (h00 : equilateral P18 P19 P06)
    (h01 : circle_circle_intersection P03 C02 C18)
    (h02 : angle_bisector_line P08 P17 P16 P27 L28)
    (h03 : angle_bisector_line P13 P20 P16 P27 L24)
    (h04 : angle_bisector_line P18 P23 P16 P27 L20)
    : triangle_pred P18 P19 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0594
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0594

theorem v06_sealed_holdout_0595
    (P02 P03 P07 P10 P12 P14 P15 P16 P19 P20 P24 P27 P29 : Point)
    (L04 L18 : Line)
    (C26 : Circle)
    (RF50 : Reflection)
    (h00 : midpoint P12 P29 P14)
    (h01 : directed_angle_eq_mod_pi P07 P02 P29 P24 P19 P14)
    (h02 : midpoint P10 P15 P20)
    (h03 : angle_bisector_line P14 P20 P16 P27 L04)
    (h04 : line_circle_intersection P03 L18 C26)
    : reflection_image RF50 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0595
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0595

theorem v06_sealed_holdout_0596
    (P02 P05 P06 P08 P11 P13 P14 P15 P16 P17 P18 P19 P20 P23 P24 P25 P27 P31 : Point)
    (L16 : Line)
    (HOM59 : Homothety)
    (h00 : between P19 P06 P25)
    (h01 : directed_angle_eq_mod_pi P14 P11 P08 P05 P02 P31)
    (h02 : area_le P17 P24 P31 P06 P13 P20)
    (h03 : angle_bisector_line P15 P20 P16 P27 L16)
    (h04 : midpoint P23 P18 P13)
    : homothety_image HOM59 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0596
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0596

theorem v06_sealed_holdout_0597
    (P03 P04 P14 P15 P16 P17 P19 P20 P25 P26 P27 : Point)
    (L02 L10 L28 : Line)
    (C02 C14 C18 C24 : Circle)
    (INV08 : Inversion)
    (h00 : area_le P26 P15 P04 P25 P14 P03)
    (h01 : line_circle_intersection P19 L10 C24)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : angle_bisector_line P16 P20 P17 P27 L28)
    (h04 : line_circle_intersection P03 L02 C14)
    : inversion_image INV08 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0597
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0597

theorem v06_sealed_holdout_0598
    (P01 P02 P06 P11 P12 P15 P16 P17 P19 P20 P22 P23 P24 P27 P28 P29 P30 : Point)
    (L10 L12 : Line)
    (C24 : Circle)
    (SP25 : SpiralSimilarity)
    (h00 : directed_angle_eq_mod_pi P01 P24 P15 P06 P29 P20)
    (h01 : midpoint P28 P29 P30)
    (h02 : angle_bisector_line P12 P17 P16 P27 L12)
    (h03 : area_le P02 P23 P12 P01 P22 P11)
    (h04 : line_circle_intersection P19 L10 C24)
    : spiral_similarity_center SP25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0598
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0598

theorem v06_sealed_holdout_0599
    (P08 P11 P12 P13 P14 P15 P16 P17 P18 P19 P28 P31 : Point)
    (L27 : Line)
    (C03 : Circle)
    (h00 : P11 = P08)
    (h01 : P18 = P19)
    (h02 : P28 = P31)
    (h03 : line_circle_intersection P15 L27 C03)
    (h04 : area_le P12 P13 P14 P15 P16 P17)
    : rotation_preserves_collinear P11 P18 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0599
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0599

theorem v06_sealed_holdout_0600
    (P02 P04 P09 P10 P13 P14 P15 P16 P17 P19 P20 P22 P25 P27 P28 P31 : Point)
    (L04 : Line)
    (C11 : Circle)
    (h00 : circle_with_center_through_point P20 P04 C11)
    (h01 : between P10 P15 P20)
    (h02 : angle_bisector_line P14 P17 P16 P27 L04)
    (h03 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    (h04 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    : on_circle P04 C11 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0600
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0600

theorem v06_sealed_holdout_0601
    (P03 P12 P18 P19 P27 P29 : Point)
    (L18 L21 : Line)
    (C02 C10 C14 C18 C27 : Circle)
    (h00 : line_circle_intersection P18 L21 C27)
    (h01 : line_circle_intersection P03 L18 C18)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : midpoint P29 P12 P27)
    : on_circle P18 C27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0601
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0601

theorem v06_sealed_holdout_0602
    (P01 P03 P07 P14 P15 P17 P19 P20 P23 P24 P26 P27 P28 P30 P31 : Point)
    (L10 L16 : Line)
    (C00 C20 : Circle)
    (h00 : chord P15 P03 C20)
    (h01 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    (h02 : between P30 P27 P24)
    (h03 : line_circle_intersection P19 L10 C00)
    (h04 : angle_bisector_line P31 P23 P17 P28 L16)
    : on_circle P15 C20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0602
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0602

theorem v06_sealed_holdout_0603
    (P03 P04 P05 P08 P10 P13 P17 P18 P19 P24 P26 P27 P28 : Point)
    (L08 L26 : Line)
    (C02 C28 : Circle)
    (h00 : tangent_chord_angle P24 P10 P27 L26 C02)
    (h01 : angle_bisector_line P17 P13 P18 P28 L08)
    (h02 : between P05 P04 P03)
    (h03 : midpoint P08 P17 P26)
    (h04 : line_circle_intersection P19 L26 C28)
    : on_circle P27 C02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0603
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0603

theorem v06_sealed_holdout_0604
    (P03 P06 P07 P14 P15 P16 P17 P18 P19 P20 P21 P23 P26 P27 P28 P29 : Point)
    (L12 L15 L18 : Line)
    (C02 : Circle)
    (h00 : altitude P26 P20 P14 P23 L15)
    (h01 : line_circle_intersection P03 L18 C02)
    (h02 : angle_bisector_line P28 P15 P18 P29 L12)
    (h03 : directed_angle_eq_mod_pi P18 P07 P28 P17 P06 P27)
    (h04 : area_le P21 P20 P19 P18 P17 P16)
    : on_line P14 L15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0604
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0604

theorem v06_sealed_holdout_0605
    (P02 P03 P09 P13 P16 P19 P21 P22 P23 P25 P28 P31 : Point)
    (L09 : Line)
    (C02 C18 C22 C26 : Circle)
    (h00 : altitude P22 P21 P13 P23 L09)
    (h01 : between P16 P09 P02)
    (h02 : area_le P19 P22 P25 P28 P31 P02)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : circle_circle_intersection P19 C22 C02)
    : on_line P13 L09 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0605
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0605

theorem v06_sealed_holdout_0606
    (P03 P04 P09 P12 P14 P18 P19 P22 P23 P26 P27 P29 P31 : Point)
    (L03 : Line)
    (C02 C14 C18 C19 : Circle)
    (h00 : altitude P18 P22 P12 P23 L03)
    (h01 : circle_circle_intersection P03 C18 C19)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    (h04 : midpoint P29 P12 P27)
    : on_line P12 L03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0606
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0606

theorem v06_sealed_holdout_0607
    (P03 P04 P06 P08 P17 P19 P21 P23 P25 P28 : Point)
    (L02 L10 L12 : Line)
    (C02 C14 C22 C28 : Circle)
    (h00 : line_circle_intersection P04 L10 C28)
    (h01 : line_circle_intersection P03 L02 C14)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    (h04 : angle_bisector_line P04 P23 P17 P28 L12)
    : on_line P04 L10 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0607
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0607

theorem v06_sealed_holdout_0608
    (P00 P01 P02 P03 P04 P05 P08 P10 P11 P14 P17 P23 P30 : Point)
    (C02 C18 : Circle)
    (h00 : equilateral P17 P14 P01)
    (h01 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : area_le P11 P30 P17 P04 P23 P10)
    (h04 : midpoint P14 P11 P08)
    : equal_length P17 P14 P14 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0608
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0608

theorem v06_sealed_holdout_0609
    (P00 P03 P05 P09 P13 P14 P15 P19 P23 P28 : Point)
    (L02 L18 : Line)
    (C02 C06 C14 : Circle)
    (h00 : equilateral P13 P15 P00)
    (h01 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h02 : line_circle_intersection P03 L18 C02)
    (h03 : circle_circle_intersection P19 C14 C02)
    (h04 : line_circle_intersection P03 L02 C06)
    : equal_length P13 P15 P15 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0609
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0609

theorem v06_sealed_holdout_0610
    (P00 P02 P03 P04 P07 P09 P10 P12 P16 P18 P19 P21 P22 P23 P25 P28 P29 P30 P31 : Point)
    (h00 : length_sum P18 P00 P30 P09 P16 P23)
    (h01 : between P21 P04 P19)
    (h02 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    (h03 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    (h04 : area_le P25 P16 P07 P30 P21 P12)
    : length_sum P30 P09 P18 P00 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0610
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0610

theorem v06_sealed_holdout_0611
    (P00 P05 P11 P12 P13 P15 P16 P17 P18 P25 P27 P28 P29 P30 : Point)
    (h00 : equal_length P15 P11 P16 P27)
    (h01 : equal_length P16 P27 P05 P17)
    (h02 : area_le P28 P13 P30 P15 P00 P17)
    (h03 : midpoint P29 P12 P27)
    (h04 : between P00 P25 P18)
    : equal_length P15 P11 P05 P17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0611
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0611

theorem v06_sealed_holdout_0612
    (P02 P03 P04 P09 P12 P13 P15 P19 P22 P23 P24 P28 : Point)
    (L18 : Line)
    (C02 C14 C18 : Circle)
    (h00 : area_eq P04 P15 P22 P02 P12 P23)
    (h01 : area_eq P02 P12 P23 P03 P13 P24)
    (h02 : directed_angle_eq_mod_pi P03 P22 P09 P28 P15 P02)
    (h03 : line_circle_intersection P03 L18 C18)
    (h04 : circle_circle_intersection P19 C14 C02)
    : area_eq P04 P15 P22 P03 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0612
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0612

theorem v06_sealed_holdout_0613
    (P03 P05 P11 P15 P16 P17 P19 P23 P27 : Point)
    (L13 : Line)
    (C02 C17 C18 C26 C30 : Circle)
    (h00 : equal_length P17 P11 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : line_circle_intersection P23 L13 C17)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : circle_circle_intersection P03 C26 C18)
    : equal_length P17 P11 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0613
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0613

theorem v06_sealed_holdout_0614
    (P03 P05 P07 P15 P18 P19 P25 P26 P28 : Point)
    (L02 : Line)
    (C02 C06 C18 : Circle)
    (h00 : angle_bisector_line P07 P28 P25 P03 L02)
    (h01 : between P15 P26 P05)
    (h02 : midpoint P18 P07 P28)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : circle_circle_intersection P03 C02 C18)
    : angle_bisector P07 P28 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0614
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0614

theorem v06_sealed_holdout_0615
    (P03 P04 P07 P10 P12 P16 P19 P21 P22 P23 P24 P25 P28 P29 P30 : Point)
    (L00 : Line)
    (h00 : angle_bisector_line P03 P29 P24 P04 L00)
    (h01 : between P19 P22 P25)
    (h02 : area_le P22 P03 P16 P29 P10 P23)
    (h03 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h04 : between P28 P29 P30)
    : angle_bisector P03 P29 P24 P04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0615
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0615

theorem v06_sealed_holdout_0616
    (P00 P03 P04 P05 P06 P07 P08 P09 P10 P11 P12 P15 P16 P18 P23 P24 P25 P27 P29 P31 : Point)
    (h00 : directed_angle_eq_mod_pi P12 P04 P05 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : area_le P29 P12 P27 P10 P25 P08)
    (h03 : area_le P00 P25 P18 P11 P04 P29)
    (h04 : between P03 P06 P09)
    : directed_angle_eq_mod_pi P12 P04 P05 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0616
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0616

theorem v06_sealed_holdout_0617
    (P00 P01 P02 P03 P06 P07 P08 P10 P16 P19 P21 P25 P30 : Point)
    (C02 C10 C14 C18 : Circle)
    (h00 : directed_angle_eq_mod_2pi P01 P08 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : between P06 P03 P00)
    (h03 : circle_circle_intersection P19 C14 C02)
    (h04 : circle_circle_intersection P03 C10 C18)
    : directed_angle_eq_mod_2pi P01 P08 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0617
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0617

theorem v06_sealed_holdout_0618
    (P04 P05 P07 P08 P10 P11 P14 P15 P16 P17 P23 P24 P30 P31 : Point)
    (h00 : directed_angle_eq_mod_pi P14 P04 P05 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : area_le P11 P30 P17 P04 P23 P10)
    (h03 : midpoint P14 P11 P08)
    (h04 : between P17 P24 P31)
    : directed_angle_eq_mod_pi P14 P04 P05 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0618
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0618

theorem v06_sealed_holdout_0619
    (P01 P02 P03 P05 P07 P08 P10 P16 P17 P18 P19 P20 P21 P22 P23 P24 P25 P28 P30 : Point)
    (h00 : directed_angle_eq_mod_2pi P03 P08 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : directed_angle_eq_mod_pi P20 P21 P22 P23 P24 P25)
    (h03 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    (h04 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    : directed_angle_eq_mod_2pi P03 P08 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0619
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0619

theorem v06_sealed_holdout_0620
    (P00 P01 P03 P07 P10 P11 P12 P16 P19 P21 P22 P24 P25 P28 P29 P30 P31 : Point)
    (L02 : Line)
    (C03 C30 : Circle)
    (h00 : circle_through_three_noncollinear_points P24 P19 P16 C03)
    (h01 : line_circle_intersection P03 L02 C30)
    (h02 : area_le P25 P16 P07 P30 P21 P12)
    (h03 : area_le P28 P29 P30 P31 P00 P01)
    (h04 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    : triangle_pred P24 P19 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0620
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0620

theorem v06_sealed_holdout_0621
    (P03 P06 P09 P13 P15 P16 P18 P19 P24 P27 P30 : Point)
    (L00 L04 L24 : Line)
    (h00 : equilateral P13 P19 P06)
    (h01 : angle_bisector_line P30 P15 P16 P27 L04)
    (h02 : angle_bisector_line P03 P18 P16 P27 L00)
    (h03 : midpoint P03 P06 P09)
    (h04 : angle_bisector_line P13 P24 P16 P27 L24)
    : triangle_pred P13 P19 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0621
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0621

theorem v06_sealed_holdout_0622
    (P02 P03 P07 P09 P14 P16 P19 P21 P24 P26 P27 P29 : Point)
    (L04 L08 : Line)
    (C17 C18 C19 : Circle)
    (h00 : circle_through_three_noncollinear_points P26 P19 P16 C17)
    (h01 : circle_circle_intersection P03 C18 C19)
    (h02 : between P07 P02 P29)
    (h03 : angle_bisector_line P09 P21 P16 P27 L08)
    (h04 : angle_bisector_line P14 P24 P16 P27 L04)
    : triangle_pred P26 P19 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0622
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0622

theorem v06_sealed_holdout_0623
    (P05 P06 P07 P08 P09 P11 P13 P14 P15 P17 P19 P20 P22 P24 P30 P31 : Point)
    (h00 : equilateral P15 P19 P06)
    (h01 : midpoint P11 P30 P17)
    (h02 : between P14 P11 P08)
    (h03 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    (h04 : directed_angle_eq_mod_pi P20 P05 P22 P07 P24 P09)
    : triangle_pred P15 P19 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0623
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0623

theorem v06_sealed_holdout_0624
    (P01 P05 P06 P07 P10 P16 P17 P18 P19 P20 P21 P24 P28 : Point)
    (L26 : Line)
    (C28 : Circle)
    (h00 : equilateral P16 P19 P06)
    (h01 : between P18 P07 P28)
    (h02 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    (h03 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    (h04 : line_circle_intersection P19 L26 C28)
    : triangle_pred P16 P19 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0624
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0624

theorem v06_sealed_holdout_0625
    (P00 P01 P02 P05 P07 P11 P12 P16 P18 P19 P21 P23 P24 P25 P28 P29 P30 P31 : Point)
    (C02 C14 : Circle)
    (RF04 : Reflection)
    (h00 : area_le P30 P11 P24 P05 P18 P31)
    (h01 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h02 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    (h03 : circle_circle_intersection P19 C14 C02)
    (h04 : between P02 P23 P12)
    : reflection_image RF04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0625
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0625

theorem v06_sealed_holdout_0626
    (P00 P01 P03 P05 P06 P09 P13 P16 P18 P20 P21 P23 P27 : Point)
    (L24 : Line)
    (C02 C18 : Circle)
    (HOM09 : Homothety)
    (h00 : directed_angle_eq_mod_pi P05 P20 P03 P18 P01 P16)
    (h01 : circle_circle_intersection P03 C02 C18)
    (h02 : midpoint P03 P06 P09)
    (h03 : angle_bisector_line P13 P21 P16 P27 L24)
    (h04 : between P09 P00 P23)
    : homothety_image HOM09 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0626
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0626

theorem v06_sealed_holdout_0627
    (P02 P03 P07 P09 P10 P11 P13 P14 P15 P19 P20 P24 P26 P28 P29 P31 : Point)
    (L18 L31 : Line)
    (C26 C31 : Circle)
    (INV18 : Inversion)
    (h00 : line_circle_intersection P31 L31 C31)
    (h01 : area_le P07 P02 P29 P24 P19 P14)
    (h02 : between P10 P15 P20)
    (h03 : area_le P13 P28 P11 P26 P09 P24)
    (h04 : line_circle_intersection P03 L18 C26)
    : inversion_image INV18 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0627
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0627

theorem v06_sealed_holdout_0628
    (P03 P05 P06 P08 P11 P13 P17 P18 P20 P22 P23 P24 P30 P31 : Point)
    (C18 C22 C26 : Circle)
    (SP31 : SpiralSimilarity)
    (h00 : circle_circle_intersection P11 C22 C26)
    (h01 : circle_circle_intersection P03 C26 C18)
    (h02 : area_le P17 P24 P31 P06 P13 P20)
    (h03 : midpoint P20 P05 P22)
    (h04 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    : spiral_similarity_center SP31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0628
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0628

theorem v06_sealed_holdout_0629
    (P01 P08 P09 P13 P15 P18 P19 P20 P21 P24 P25 P27 P28 P30 P31 : Point)
    (L28 : Line)
    (h00 : P09 = P08)
    (h01 : P19 = P20)
    (h02 : P28 = P31)
    (h03 : angle_bisector_line P01 P25 P31 P13 L28)
    (h04 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    : rotation_preserves_collinear P09 P19 P28 P08 P20 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0629
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0629

theorem v06_sealed_holdout_0630
    (P02 P05 P10 P12 P18 P19 P21 P23 P28 P29 P30 P31 : Point)
    (L10 : Line)
    (C15 C24 : Circle)
    (h00 : circle_with_center_through_point P18 P05 C15)
    (h01 : midpoint P28 P29 P30)
    (h02 : between P31 P10 P21)
    (h03 : between P02 P23 P12)
    (h04 : line_circle_intersection P19 L10 C24)
    : on_circle P05 C15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0630
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0630

theorem v06_sealed_holdout_0631
    (P00 P05 P09 P12 P13 P14 P15 P16 P17 P23 P26 P28 : Point)
    (L21 L24 : Line)
    (C09 : Circle)
    (h00 : line_circle_intersection P16 L21 C09)
    (h01 : angle_bisector_line P13 P14 P17 P28 L24)
    (h02 : between P09 P00 P23)
    (h03 : between P12 P13 P14)
    (h04 : between P15 P26 P05)
    : on_circle P16 C09 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0631
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0631

theorem v06_sealed_holdout_0632
    (P03 P04 P09 P11 P13 P17 P18 P19 P22 P24 P25 P26 P28 : Point)
    (L00 : Line)
    (C18 C26 C28 : Circle)
    (h00 : chord P13 P04 C28)
    (h01 : area_le P13 P28 P11 P26 P09 P24)
    (h02 : angle_bisector_line P19 P17 P18 P28 L00)
    (h03 : between P19 P22 P25)
    (h04 : circle_circle_intersection P03 C26 C18)
    : on_circle P13 C28 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0632
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0632

theorem v06_sealed_holdout_0633
    (P00 P03 P04 P08 P09 P10 P12 P14 P18 P19 P25 P26 P27 P29 P31 : Point)
    (L01 L26 : Line)
    (C04 C20 : Circle)
    (h00 : line_circle_intersection P03 L01 C20)
    (h01 : line_circle_intersection P19 L26 C04)
    (h02 : area_le P26 P31 P04 P09 P14 P19)
    (h03 : directed_angle_eq_mod_pi P29 P12 P27 P10 P25 P08)
    (h04 : midpoint P00 P25 P18)
    : on_line P03 L01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0633
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0633

theorem v06_sealed_holdout_0634
    (P02 P04 P06 P07 P08 P14 P15 P18 P19 P21 P23 P24 P25 P27 P29 P30 : Point)
    (L21 : Line)
    (C02 C22 : Circle)
    (h00 : altitude P24 P21 P14 P23 L21)
    (h01 : area_le P30 P27 P24 P21 P18 P15)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : area_le P04 P21 P06 P23 P08 P25)
    (h04 : midpoint P07 P02 P29)
    : on_line P14 L21 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0634
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0634

theorem v06_sealed_holdout_0635
    (P01 P02 P03 P04 P05 P08 P11 P12 P13 P17 P19 P20 P21 P22 P23 P26 : Point)
    (L15 : Line)
    (C02 C30 : Circle)
    (h00 : altitude P20 P22 P13 P23 L15)
    (h01 : area_le P02 P23 P12 P01 P22 P11)
    (h02 : between P05 P04 P03)
    (h03 : directed_angle_eq_mod_pi P08 P17 P26 P03 P12 P21)
    (h04 : circle_circle_intersection P19 C30 C02)
    : on_line P13 L15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0635
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0635

theorem v06_sealed_holdout_0636
    (P03 P05 P06 P12 P13 P14 P15 P16 P17 P18 P19 P23 P24 P26 P27 : Point)
    (L02 L09 L20 : Line)
    (C30 : Circle)
    (h00 : altitude P16 P23 P12 P24 L09)
    (h01 : line_circle_intersection P03 L02 C30)
    (h02 : angle_bisector_line P18 P19 P16 P27 L20)
    (h03 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h04 : area_le P15 P26 P05 P16 P27 P06)
    : on_line P12 L09 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0636
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0636

theorem v06_sealed_holdout_0637
    (P02 P03 P07 P09 P10 P16 P19 P22 P23 P25 P28 P29 P31 : Point)
    (L12 : Line)
    (C12 : Circle)
    (h00 : line_circle_intersection P02 L12 C12)
    (h01 : midpoint P16 P09 P02)
    (h02 : area_le P19 P22 P25 P28 P31 P02)
    (h03 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    (h04 : between P25 P16 P07)
    : on_line P02 L12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0637
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0637

theorem v06_sealed_holdout_0638
    (P01 P03 P13 P15 P16 P18 P19 P23 : Point)
    (L02 : Line)
    (C02 C06 C18 C22 : Circle)
    (h00 : equilateral P15 P16 P01)
    (h01 : midpoint P23 P18 P13)
    (h02 : line_circle_intersection P03 L02 C22)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : circle_circle_intersection P03 C02 C18)
    : equal_length P15 P16 P16 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0638
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0638

theorem v06_sealed_holdout_0639
    (P00 P01 P04 P06 P08 P11 P15 P16 P19 P21 P24 P27 P30 : Point)
    (C02 C30 : Circle)
    (h00 : equilateral P11 P16 P00)
    (h01 : circle_circle_intersection P19 C30 C02)
    (h02 : between P30 P27 P24)
    (h03 : between P01 P08 P15)
    (h04 : between P04 P21 P06)
    : equal_length P11 P16 P16 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0639
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0639

theorem v06_sealed_holdout_0640
    (P00 P01 P02 P03 P04 P05 P07 P08 P09 P16 P17 P18 P19 P23 P25 P27 P29 P30 : Point)
    (L28 : Line)
    (C02 C18 : Circle)
    (h00 : length_sum P16 P01 P30 P09 P17 P23)
    (h01 : directed_angle_eq_mod_pi P07 P18 P29 P08 P19 P30)
    (h02 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : angle_bisector_line P00 P25 P16 P27 L28)
    : length_sum P30 P09 P16 P01 P17 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0640
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0640

theorem v06_sealed_holdout_0641
    (P03 P05 P06 P07 P12 P13 P15 P16 P26 P27 : Point)
    (L17 : Line)
    (C10 C13 C18 : Circle)
    (h00 : equal_length P13 P12 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : line_circle_intersection P07 L17 C13)
    (h03 : area_le P15 P26 P05 P16 P27 P06)
    (h04 : circle_circle_intersection P03 C10 C18)
    : equal_length P13 P12 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0641
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0641

theorem v06_sealed_holdout_0642
    (P02 P03 P04 P07 P12 P13 P16 P19 P22 P23 P24 P25 : Point)
    (C02 C06 C18 C26 : Circle)
    (h00 : area_eq P02 P16 P22 P03 P12 P23)
    (h01 : area_eq P03 P12 P23 P04 P13 P24)
    (h02 : circle_circle_intersection P19 C06 C02)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : midpoint P25 P16 P07)
    : area_eq P02 P16 P22 P04 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0642
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0642

theorem v06_sealed_holdout_0643
    (P00 P04 P05 P11 P12 P13 P15 P16 P17 P18 P19 P25 P27 P29 P31 : Point)
    (L10 L12 : Line)
    (C08 : Circle)
    (h00 : equal_length P15 P12 P16 P27)
    (h01 : equal_length P16 P27 P05 P17)
    (h02 : angle_bisector_line P15 P25 P31 P13 L12)
    (h03 : line_circle_intersection P19 L10 C08)
    (h04 : area_le P00 P25 P18 P11 P04 P29)
    : equal_length P15 P12 P05 P17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0643
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0643

theorem v06_sealed_holdout_0644
    (P01 P02 P03 P04 P05 P06 P07 P08 P10 P15 P20 P21 P22 P25 P29 P30 : Point)
    (L04 : Line)
    (h00 : angle_bisector_line P05 P29 P25 P03 L04)
    (h01 : area_le P01 P08 P15 P22 P29 P04)
    (h02 : midpoint P04 P21 P06)
    (h03 : between P07 P02 P29)
    (h04 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    : angle_bisector P05 P29 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0644
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0644

theorem v06_sealed_holdout_0645
    (P00 P01 P02 P03 P04 P05 P11 P16 P17 P18 P24 P27 P28 P30 : Point)
    (L00 L02 : Line)
    (C14 : Circle)
    (h00 : angle_bisector_line P01 P30 P24 P03 L02)
    (h01 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    (h02 : angle_bisector_line P27 P18 P16 P28 L00)
    (h03 : between P11 P30 P17)
    (h04 : line_circle_intersection P03 L02 C14)
    : angle_bisector P01 P30 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0645
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0645

theorem v06_sealed_holdout_0646
    (P04 P05 P06 P07 P10 P15 P16 P18 P23 P24 P25 P27 P28 P31 : Point)
    (L04 L12 : Line)
    (h00 : directed_angle_eq_mod_pi P10 P05 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : angle_bisector_line P28 P18 P16 P27 L12)
    (h03 : between P18 P07 P28)
    (h04 : angle_bisector_line P06 P25 P16 P27 L04)
    : directed_angle_eq_mod_pi P10 P05 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0646
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0646

theorem v06_sealed_holdout_0647
    (P00 P01 P02 P03 P07 P09 P10 P16 P17 P21 P24 P25 P28 P29 P30 P31 : Point)
    (h00 : directed_angle_eq_mod_2pi P31 P09 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : directed_angle_eq_mod_pi P24 P17 P10 P03 P28 P21)
    (h03 : midpoint P25 P16 P07)
    (h04 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    : directed_angle_eq_mod_2pi P31 P09 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0647
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0647

theorem v06_sealed_holdout_0648
    (P00 P04 P05 P07 P08 P10 P11 P12 P15 P16 P18 P19 P23 P24 P25 P27 P29 P31 : Point)
    (L26 : Line)
    (C12 : Circle)
    (h00 : directed_angle_eq_mod_pi P12 P05 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : area_le P29 P12 P27 P10 P25 P08)
    (h03 : area_le P00 P25 P18 P11 P04 P29)
    (h04 : line_circle_intersection P19 L26 C12)
    : directed_angle_eq_mod_pi P12 P05 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0648
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0648

theorem v06_sealed_holdout_0649
    (P01 P02 P03 P07 P09 P10 P15 P16 P20 P21 P25 P29 P30 : Point)
    (C22 C30 : Circle)
    (h00 : directed_angle_eq_mod_2pi P01 P09 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : circle_circle_intersection P07 C30 C22)
    (h03 : midpoint P07 P02 P29)
    (h04 : area_le P10 P15 P20 P25 P30 P03)
    : directed_angle_eq_mod_2pi P01 P09 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0649
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0649

theorem v06_sealed_holdout_0650
    (P00 P06 P08 P11 P13 P14 P16 P17 P19 P20 P22 P24 P26 P27 P31 : Point)
    (L28 : Line)
    (C21 : Circle)
    (h00 : circle_through_three_noncollinear_points P22 P20 P16 C21)
    (h01 : midpoint P08 P17 P26)
    (h02 : angle_bisector_line P00 P19 P16 P27 L28)
    (h03 : between P14 P11 P08)
    (h04 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    : triangle_pred P22 P20 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0650
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0650

theorem v06_sealed_holdout_0651
    (P01 P06 P07 P10 P11 P18 P19 P20 P21 P24 P28 : Point)
    (L26 : Line)
    (C20 : Circle)
    (h00 : equilateral P11 P20 P06)
    (h01 : line_circle_intersection P19 L26 C20)
    (h02 : between P18 P07 P28)
    (h03 : midpoint P21 P20 P19)
    (h04 : between P24 P01 P10)
    : triangle_pred P11 P20 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0651
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0651

theorem v06_sealed_holdout_0652
    (P03 P07 P10 P12 P16 P20 P21 P22 P23 P24 P25 P27 P29 P30 : Point)
    (L12 : Line)
    (C03 C18 C19 : Circle)
    (h00 : circle_through_three_noncollinear_points P24 P20 P16 C03)
    (h01 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    (h02 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h03 : circle_circle_intersection P03 C18 C19)
    (h04 : angle_bisector_line P12 P25 P16 P27 L12)
    : triangle_pred P24 P20 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0652
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0652

theorem v06_sealed_holdout_0653
    (P00 P03 P04 P06 P08 P09 P10 P11 P12 P13 P15 P18 P19 P20 P25 P27 P29 : Point)
    (h00 : equilateral P13 P20 P06)
    (h01 : directed_angle_eq_mod_pi P29 P12 P27 P10 P25 P08)
    (h02 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    (h03 : area_le P03 P06 P09 P12 P15 P18)
    (h04 : between P06 P19 P00)
    : triangle_pred P13 P20 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0653
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0653

theorem v06_sealed_holdout_0654
    (P02 P04 P06 P07 P09 P14 P16 P19 P20 P21 P22 P27 P29 : Point)
    (L08 : Line)
    (C02 C06 : Circle)
    (h00 : equilateral P14 P20 P06)
    (h01 : between P04 P21 P06)
    (h02 : between P07 P02 P29)
    (h03 : angle_bisector_line P09 P22 P16 P27 L08)
    (h04 : circle_circle_intersection P19 C06 C02)
    : triangle_pred P14 P20 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0654
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0654

theorem v06_sealed_holdout_0655
    (P03 P05 P06 P08 P11 P12 P13 P14 P17 P19 P20 P21 P22 P24 P26 P31 : Point)
    (C02 C30 : Circle)
    (RF22 : Reflection)
    (h00 : area_le P08 P17 P26 P03 P12 P21)
    (h01 : circle_circle_intersection P19 C30 C02)
    (h02 : midpoint P14 P11 P08)
    (h03 : area_le P17 P24 P31 P06 P13 P20)
    (h04 : midpoint P20 P05 P22)
    : reflection_image RF22 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0655
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0655

theorem v06_sealed_holdout_0656
    (P01 P03 P05 P06 P10 P15 P16 P17 P18 P19 P20 P21 P24 P26 P27 : Point)
    (L02 : Line)
    (C02 C06 C30 : Circle)
    (HOM23 : Homothety)
    (h00 : area_le P15 P26 P05 P16 P27 P06)
    (h01 : line_circle_intersection P03 L02 C06)
    (h02 : area_le P21 P20 P19 P18 P17 P16)
    (h03 : midpoint P24 P01 P10)
    (h04 : circle_circle_intersection P19 C30 C02)
    : homothety_image HOM23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0656
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0656

theorem v06_sealed_holdout_0657
    (P02 P03 P07 P10 P12 P16 P21 P22 P23 P25 P28 P29 P30 P31 : Point)
    (INV28 : Inversion)
    (h00 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    (h01 : area_le P25 P16 P07 P30 P21 P12)
    (h02 : between P28 P29 P30)
    (h03 : between P31 P10 P21)
    (h04 : between P02 P23 P12)
    : inversion_image INV28 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0657
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0657

theorem v06_sealed_holdout_0658
    (P00 P03 P06 P07 P09 P12 P13 P16 P17 P19 P23 P26 P27 P29 : Point)
    (L00 : Line)
    (C02 C30 : Circle)
    (SP37 : SpiralSimilarity)
    (h00 : midpoint P29 P12 P27)
    (h01 : angle_bisector_line P03 P16 P17 P27 L00)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : area_le P06 P19 P00 P13 P26 P07)
    (h04 : between P09 P00 P23)
    : spiral_similarity_center SP37 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0658
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0658

theorem v06_sealed_holdout_0659
    (P02 P07 P08 P09 P11 P13 P16 P19 P20 P27 P28 P31 : Point)
    (h00 : P07 = P08)
    (h01 : P20 = P19)
    (h02 : P28 = P31)
    (h03 : between P13 P28 P11)
    (h04 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    : rotation_preserves_collinear P07 P20 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0659
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0659

theorem v06_sealed_holdout_0660
    (P03 P05 P06 P13 P16 P17 P18 P23 P24 P27 P31 : Point)
    (L18 L24 : Line)
    (C18 C19 : Circle)
    (h00 : circle_with_center_through_point P16 P06 C19)
    (h01 : angle_bisector_line P05 P16 P17 P27 L24)
    (h02 : midpoint P17 P24 P31)
    (h03 : line_circle_intersection P03 L18 C18)
    (h04 : midpoint P23 P18 P13)
    : on_circle P06 C19 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0660
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0660

theorem v06_sealed_holdout_0661
    (P01 P03 P08 P11 P14 P15 P17 P19 P28 : Point)
    (L00 L02 L21 L26 : Line)
    (C14 C23 C28 : Circle)
    (h00 : line_circle_intersection P14 L21 C23)
    (h01 : angle_bisector_line P11 P15 P17 P28 L00)
    (h02 : line_circle_intersection P19 L26 C28)
    (h03 : line_circle_intersection P03 L02 C14)
    (h04 : midpoint P01 P08 P15)
    : on_circle P14 C23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0661
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0661

theorem v06_sealed_holdout_0662
    (P02 P03 P05 P10 P11 P12 P19 P21 P23 P31 : Point)
    (L18 : Line)
    (C02 C04 C06 C10 : Circle)
    (h00 : chord P11 P05 C04)
    (h01 : midpoint P31 P10 P21)
    (h02 : midpoint P02 P23 P12)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : line_circle_intersection P03 L18 C10)
    : on_circle P11 C04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0662
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0662

theorem v06_sealed_holdout_0663
    (P00 P03 P06 P07 P09 P12 P13 P19 P20 P23 P26 P27 : Point)
    (L18 : Line)
    (C02 C10 C14 C18 C19 : Circle)
    (h00 : tangent_chord_angle P20 P12 P27 L18 C10)
    (h01 : area_le P06 P19 P00 P13 P26 P07)
    (h02 : between P09 P00 P23)
    (h03 : circle_circle_intersection P03 C18 C19)
    (h04 : circle_circle_intersection P19 C14 C02)
    : on_circle P27 C10 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0663
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0663

theorem v06_sealed_holdout_0664
    (P02 P03 P10 P14 P16 P19 P22 P23 P24 P25 P28 P29 P31 : Point)
    (L27 : Line)
    (C02 C18 C22 : Circle)
    (h00 : altitude P22 P23 P14 P24 L27)
    (h01 : circle_circle_intersection P03 C02 C18)
    (h02 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    (h03 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    (h04 : circle_circle_intersection P19 C22 C02)
    : on_line P14 L27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0664
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0664

theorem v06_sealed_holdout_0665
    (P04 P05 P09 P12 P13 P14 P18 P19 P20 P22 P23 P24 P26 P27 P29 P31 : Point)
    (L21 L26 : Line)
    (C04 : Circle)
    (h00 : altitude P18 P23 P13 P24 L21)
    (h01 : between P20 P05 P22)
    (h02 : line_circle_intersection P19 L26 C04)
    (h03 : area_le P26 P31 P04 P09 P14 P19)
    (h04 : midpoint P29 P12 P27)
    : on_line P13 L21 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0665
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0665

theorem v06_sealed_holdout_0666
    (P03 P12 P14 P16 P17 P19 P23 P24 P27 P30 : Point)
    (L10 L15 L18 L28 : Line)
    (C00 C10 : Circle)
    (h00 : altitude P14 P24 P12 P23 L15)
    (h01 : line_circle_intersection P03 L18 C10)
    (h02 : angle_bisector_line P16 P19 P17 P27 L28)
    (h03 : between P30 P27 P24)
    (h04 : line_circle_intersection P19 L10 C00)
    : on_line P12 L15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0666
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0666

theorem v06_sealed_holdout_0667
    (P00 P02 P03 P11 P12 P17 P19 P23 P30 : Point)
    (L14 : Line)
    (C02 C06 C18 C28 : Circle)
    (h00 : line_circle_intersection P00 L14 C28)
    (h01 : midpoint P02 P23 P12)
    (h02 : circle_circle_intersection P19 C06 C02)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : between P11 P30 P17)
    : on_line P00 L14 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0667
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0667

theorem v06_sealed_holdout_0668
    (P00 P01 P05 P06 P07 P09 P12 P13 P14 P15 P16 P17 P18 P23 P26 P27 P28 : Point)
    (h00 : equilateral P13 P16 P01)
    (h01 : midpoint P09 P00 P23)
    (h02 : area_le P12 P13 P14 P15 P16 P17)
    (h03 : between P15 P26 P05)
    (h04 : directed_angle_eq_mod_pi P18 P07 P28 P17 P06 P27)
    : equal_length P13 P16 P16 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0668
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0668

theorem v06_sealed_holdout_0669
    (P00 P02 P09 P11 P13 P16 P17 P19 P20 P22 P25 P26 P27 P28 P29 P31 : Point)
    (L24 : Line)
    (h00 : equilateral P09 P17 P00)
    (h01 : midpoint P13 P28 P11)
    (h02 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    (h03 : area_le P19 P22 P25 P28 P31 P02)
    (h04 : angle_bisector_line P29 P26 P16 P27 L24)
    : equal_length P09 P17 P17 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0669
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0669

theorem v06_sealed_holdout_0670
    (P02 P04 P05 P07 P09 P14 P16 P19 P20 P22 P23 P24 P26 P27 P30 P31 : Point)
    (L04 L26 : Line)
    (C04 : Circle)
    (h00 : length_sum P14 P02 P30 P09 P16 P23)
    (h01 : area_le P20 P05 P22 P07 P24 P09)
    (h02 : line_circle_intersection P19 L26 C04)
    (h03 : midpoint P26 P31 P04)
    (h04 : angle_bisector_line P30 P26 P16 P27 L04)
    : length_sum P30 P09 P14 P02 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0670
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0670

theorem v06_sealed_holdout_0671
    (P04 P05 P06 P11 P13 P15 P16 P18 P19 P21 P24 P27 P30 : Point)
    (L10 : Line)
    (C00 : Circle)
    (h00 : equal_length P11 P13 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : area_le P30 P27 P24 P21 P18 P15)
    (h03 : line_circle_intersection P19 L10 C00)
    (h04 : midpoint P04 P21 P06)
    : equal_length P11 P13 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0671
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0671

theorem v06_sealed_holdout_0672
    (P00 P02 P03 P11 P12 P13 P16 P17 P19 P22 P23 P24 P27 P30 : Point)
    (L04 L18 : Line)
    (C10 : Circle)
    (h00 : area_eq P00 P17 P22 P02 P12 P23)
    (h01 : area_eq P02 P12 P23 P03 P13 P24)
    (h02 : angle_bisector_line P22 P19 P16 P27 L04)
    (h03 : line_circle_intersection P03 L18 C10)
    (h04 : between P11 P30 P17)
    : area_eq P00 P17 P22 P03 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0672
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0672

theorem v06_sealed_holdout_0673
    (P05 P06 P07 P12 P13 P14 P15 P16 P17 P18 P26 P27 P28 : Point)
    (h00 : equal_length P13 P14 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : area_le P12 P13 P14 P15 P16 P17)
    (h03 : between P15 P26 P05)
    (h04 : directed_angle_eq_mod_pi P18 P07 P28 P17 P06 P27)
    : equal_length P13 P14 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0673
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0673

theorem v06_sealed_holdout_0674
    (P02 P03 P04 P07 P10 P15 P16 P17 P22 P23 P24 P25 P28 P29 P30 : Point)
    (L06 L16 L20 L28 : Line)
    (h00 : angle_bisector_line P03 P30 P25 P04 L06)
    (h01 : angle_bisector_line P24 P15 P17 P28 L28)
    (h02 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    (h03 : angle_bisector_line P02 P22 P17 P28 L20)
    (h04 : angle_bisector_line P07 P25 P17 P28 L16)
    : angle_bisector P03 P30 P25 P04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0674
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0674

theorem v06_sealed_holdout_0675
    (P00 P03 P08 P12 P13 P18 P23 P24 P25 P27 P29 P30 P31 : Point)
    (L02 L04 : Line)
    (C22 : Circle)
    (h00 : angle_bisector_line P31 P00 P24 P03 L04)
    (h01 : area_le P23 P18 P13 P08 P03 P30)
    (h02 : line_circle_intersection P03 L02 C22)
    (h03 : midpoint P29 P12 P27)
    (h04 : between P00 P25 P18)
    : angle_bisector P31 P00 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0675
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0675

theorem v06_sealed_holdout_0676
    (P01 P02 P04 P06 P07 P08 P15 P16 P21 P23 P24 P29 P31 : Point)
    (h00 : directed_angle_eq_mod_pi P08 P06 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : between P01 P08 P15)
    (h03 : midpoint P04 P21 P06)
    (h04 : midpoint P07 P02 P29)
    : directed_angle_eq_mod_pi P08 P06 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0676
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0676

theorem v06_sealed_holdout_0677
    (P02 P03 P05 P07 P08 P10 P11 P14 P16 P17 P21 P25 P29 P30 P31 : Point)
    (L18 : Line)
    (C10 : Circle)
    (h00 : directed_angle_eq_mod_2pi P29 P10 P11 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : line_circle_intersection P03 L18 C10)
    (h03 : midpoint P11 P30 P17)
    (h04 : directed_angle_eq_mod_pi P14 P11 P08 P05 P02 P31)
    : directed_angle_eq_mod_2pi P29 P10 P11 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0677
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0677

theorem v06_sealed_holdout_0678
    (P03 P04 P05 P06 P07 P10 P15 P16 P19 P23 P24 P26 P27 P31 : Point)
    (C02 C06 C10 C18 : Circle)
    (h00 : directed_angle_eq_mod_pi P10 P06 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : directed_angle_eq_mod_pi P15 P26 P05 P16 P27 P06)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : circle_circle_intersection P19 C06 C02)
    : directed_angle_eq_mod_pi P10 P06 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0678
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0678

theorem v06_sealed_holdout_0679
    (P02 P03 P07 P10 P11 P16 P21 P22 P25 P28 P29 P30 P31 : Point)
    (h00 : directed_angle_eq_mod_2pi P31 P10 P11 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : midpoint P22 P03 P16)
    (h03 : between P25 P16 P07)
    (h04 : between P28 P29 P30)
    : directed_angle_eq_mod_2pi P31 P10 P11 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0679
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0679

theorem v06_sealed_holdout_0680
    (P00 P03 P04 P08 P11 P12 P16 P18 P20 P21 P25 P26 P27 P29 : Point)
    (L02 L28 : Line)
    (C07 C22 : Circle)
    (h00 : circle_through_three_noncollinear_points P20 P21 P16 C07)
    (h01 : line_circle_intersection P03 L02 C22)
    (h02 : midpoint P29 P12 P27)
    (h03 : area_le P00 P25 P18 P11 P04 P29)
    (h04 : angle_bisector_line P08 P26 P16 P27 L28)
    : triangle_pred P20 P21 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0680
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0680

theorem v06_sealed_holdout_0681
    (P01 P03 P04 P06 P08 P09 P10 P15 P16 P20 P21 P22 P23 P25 P27 P29 P30 : Point)
    (L12 : Line)
    (h00 : equilateral P09 P21 P06)
    (h01 : directed_angle_eq_mod_pi P01 P08 P15 P22 P29 P04)
    (h02 : midpoint P04 P21 P06)
    (h03 : angle_bisector_line P04 P23 P16 P27 L12)
    (h04 : area_le P10 P15 P20 P25 P30 P03)
    : triangle_pred P09 P21 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0681
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0681

theorem v06_sealed_holdout_0682
    (P03 P04 P05 P10 P11 P16 P17 P21 P22 P23 P26 P27 P30 : Point)
    (L20 L24 : Line)
    (C02 C18 C21 : Circle)
    (h00 : circle_through_three_noncollinear_points P22 P21 P16 C21)
    (h01 : circle_circle_intersection P03 C02 C18)
    (h02 : area_le P11 P30 P17 P04 P23 P10)
    (h03 : angle_bisector_line P05 P23 P16 P27 L24)
    (h04 : angle_bisector_line P10 P26 P16 P27 L20)
    : triangle_pred P22 P21 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0682
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0682

theorem v06_sealed_holdout_0683
    (P01 P05 P06 P07 P10 P11 P16 P17 P18 P19 P21 P24 P27 P28 : Point)
    (L10 L12 : Line)
    (C24 : Circle)
    (h00 : equilateral P11 P21 P06)
    (h01 : angle_bisector_line P28 P16 P17 P27 L12)
    (h02 : midpoint P18 P07 P28)
    (h03 : line_circle_intersection P19 L10 C24)
    (h04 : area_le P24 P01 P10 P19 P28 P05)
    : triangle_pred P11 P21 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0683
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0683

theorem v06_sealed_holdout_0684
    (P03 P06 P07 P12 P16 P19 P21 P25 P28 P29 P30 : Point)
    (L02 L26 : Line)
    (C20 C30 : Circle)
    (h00 : equilateral P12 P21 P06)
    (h01 : line_circle_intersection P03 L02 C30)
    (h02 : area_le P25 P16 P07 P30 P21 P12)
    (h03 : between P28 P29 P30)
    (h04 : line_circle_intersection P19 L26 C20)
    : triangle_pred P12 P21 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0684
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0684

theorem v06_sealed_holdout_0685
    (P00 P03 P04 P06 P07 P08 P11 P13 P16 P18 P19 P23 P25 P26 P27 P29 : Point)
    (L28 : Line)
    (C02 C06 C10 C18 : Circle)
    (RF40 : Reflection)
    (h00 : circle_circle_intersection P03 C10 C18)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : area_le P00 P25 P18 P11 P04 P29)
    (h03 : angle_bisector_line P08 P23 P16 P27 L28)
    (h04 : area_le P06 P19 P00 P13 P26 P07)
    : reflection_image RF40 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0685
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0685

theorem v06_sealed_holdout_0686
    (P01 P02 P07 P08 P09 P10 P11 P13 P15 P16 P17 P20 P24 P26 P27 P28 P29 P31 : Point)
    (L16 : Line)
    (HOM37 : Homothety)
    (h00 : between P01 P08 P15)
    (h01 : angle_bisector_line P31 P17 P16 P27 L16)
    (h02 : between P07 P02 P29)
    (h03 : midpoint P10 P15 P20)
    (h04 : area_le P13 P28 P11 P26 P09 P24)
    : homothety_image HOM37 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0686
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0686

theorem v06_sealed_holdout_0687
    (P03 P05 P08 P10 P11 P16 P17 P20 P22 P23 P26 P27 P30 : Point)
    (L02 L20 : Line)
    (C14 : Circle)
    (INV38 : Inversion)
    (h00 : midpoint P08 P17 P26)
    (h01 : midpoint P11 P30 P17)
    (h02 : line_circle_intersection P03 L02 C14)
    (h03 : angle_bisector_line P10 P23 P16 P27 L20)
    (h04 : midpoint P20 P05 P22)
    : inversion_image INV38 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0687
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0687

theorem v06_sealed_holdout_0688
    (P01 P03 P05 P07 P10 P14 P15 P16 P17 P18 P19 P20 P21 P24 P26 P27 P28 : Point)
    (C10 C18 : Circle)
    (SP43 : SpiralSimilarity)
    (h00 : midpoint P15 P26 P05)
    (h01 : circle_circle_intersection P03 C10 C18)
    (h02 : area_le P21 P20 P19 P18 P17 P16)
    (h03 : area_le P24 P01 P10 P19 P28 P05)
    (h04 : area_le P27 P14 P01 P20 P07 P26)
    : spiral_similarity_center SP43 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0688
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0688

theorem v06_sealed_holdout_0689
    (P01 P02 P05 P08 P10 P11 P12 P19 P21 P22 P23 P28 P31 : Point)
    (h00 : P05 = P08)
    (h01 : P21 = P19)
    (h02 : P28 = P31)
    (h03 : between P31 P10 P21)
    (h04 : directed_angle_eq_mod_pi P02 P23 P12 P01 P22 P11)
    : rotation_preserves_collinear P05 P21 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0689
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0689

theorem v06_sealed_holdout_0690
    (P00 P03 P06 P07 P09 P14 P19 : Point)
    (L10 : Line)
    (C02 C16 C18 C23 : Circle)
    (h00 : circle_with_center_through_point P14 P07 C23)
    (h01 : circle_circle_intersection P03 C02 C18)
    (h02 : midpoint P03 P06 P09)
    (h03 : between P06 P19 P00)
    (h04 : line_circle_intersection P19 L10 C16)
    : on_circle P07 C23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0690
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0690

theorem v06_sealed_holdout_0691
    (P02 P03 P09 P12 P14 P16 P17 P19 P24 P25 P28 : Point)
    (L04 L21 L28 : Line)
    (C05 C10 C18 : Circle)
    (h00 : line_circle_intersection P12 L21 C05)
    (h01 : circle_circle_intersection P03 C10 C18)
    (h02 : angle_bisector_line P14 P19 P17 P28 L04)
    (h03 : between P16 P09 P02)
    (h04 : angle_bisector_line P24 P25 P17 P28 L28)
    : on_circle P12 C05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0691
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0691

theorem v06_sealed_holdout_0692
    (P03 P06 P09 P17 P20 P22 P24 P28 P31 : Point)
    (L12 L18 : Line)
    (C10 C12 C18 : Circle)
    (h00 : chord P09 P06 C12)
    (h01 : midpoint P17 P24 P31)
    (h02 : line_circle_intersection P03 L18 C18)
    (h03 : angle_bisector_line P20 P22 P17 P28 L12)
    (h04 : circle_circle_intersection P03 C10 C18)
    : on_circle P09 C12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0692
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0692

theorem v06_sealed_holdout_0693
    (P01 P05 P07 P08 P10 P13 P14 P15 P18 P19 P20 P21 P24 P26 P27 P28 P30 : Point)
    (L30 : Line)
    (C14 : Circle)
    (h00 : tangent_chord_angle P18 P13 P27 L30 C14)
    (h01 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    (h02 : area_le P27 P14 P01 P20 P07 P26)
    (h03 : area_le P30 P27 P24 P21 P18 P15)
    (h04 : midpoint P01 P08 P15)
    : on_circle P27 C14 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0693
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0693

theorem v06_sealed_holdout_0694
    (P00 P01 P02 P03 P04 P05 P08 P11 P12 P14 P17 P18 P20 P22 P23 P24 P25 P26 P28 : Point)
    (L01 L28 : Line)
    (h00 : altitude P20 P23 P14 P24 L01)
    (h01 : area_le P02 P23 P12 P01 P22 P11)
    (h02 : area_le P05 P04 P03 P02 P01 P00)
    (h03 : between P08 P17 P26)
    (h04 : angle_bisector_line P00 P25 P18 P28 L28)
    : on_line P14 L01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0694
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0694

theorem v06_sealed_holdout_0695
    (P03 P13 P16 P17 P18 P19 P23 P24 P28 : Point)
    (L02 L18 L20 L26 L27 : Line)
    (C02 C20 C30 : Circle)
    (h00 : altitude P16 P24 P13 P23 L27)
    (h01 : line_circle_intersection P03 L02 C30)
    (h02 : angle_bisector_line P18 P19 P17 P28 L20)
    (h03 : line_circle_intersection P03 L18 C02)
    (h04 : line_circle_intersection P19 L26 C20)
    : on_line P13 L27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0695
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0695

theorem v06_sealed_holdout_0696
    (P02 P03 P05 P10 P11 P13 P16 P19 P22 P23 P25 P27 P28 P29 P31 : Point)
    (L12 : Line)
    (C02 C18 : Circle)
    (h00 : angle_bisector_line P05 P27 P19 P29 L12)
    (h01 : between P13 P28 P11)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : area_le P19 P22 P25 P28 P31 P02)
    (h04 : area_le P22 P03 P16 P29 P10 P23)
    : on_line P05 L12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0696
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0696

theorem v06_sealed_holdout_0697
    (P03 P04 P09 P12 P14 P19 P26 P27 P29 P30 P31 : Point)
    (L16 L18 L26 : Line)
    (C04 C12 C18 : Circle)
    (h00 : line_circle_intersection P30 L16 C12)
    (h01 : line_circle_intersection P03 L18 C18)
    (h02 : line_circle_intersection P19 L26 C04)
    (h03 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    (h04 : between P29 P12 P27)
    : on_line P30 L16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0697
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0697

theorem v06_sealed_holdout_0698
    (P01 P04 P06 P08 P11 P15 P16 P17 P18 P21 P22 P23 P24 P25 P26 P27 P28 P30 : Point)
    (L20 L28 : Line)
    (h00 : equilateral P11 P17 P01)
    (h01 : angle_bisector_line P16 P17 P18 P28 L28)
    (h02 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    (h03 : angle_bisector_line P26 P22 P17 P28 L20)
    (h04 : area_le P04 P21 P06 P23 P08 P25)
    : equal_length P11 P17 P17 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0698
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0698

theorem v06_sealed_holdout_0699
    (P00 P02 P07 P08 P12 P16 P17 P18 P19 P22 P23 P26 P27 : Point)
    (L04 : Line)
    (C02 C14 : Circle)
    (h00 : equilateral P07 P18 P00)
    (h01 : circle_circle_intersection P19 C14 C02)
    (h02 : between P02 P23 P12)
    (h03 : angle_bisector_line P22 P23 P16 P27 L04)
    (h04 : between P08 P17 P26)
    : equal_length P07 P18 P18 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0699
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0699

theorem v06_sealed_holdout_0700
    (P00 P03 P05 P09 P12 P15 P16 P23 P26 P30 : Point)
    (C18 C19 C26 : Circle)
    (h00 : length_sum P12 P03 P30 P09 P16 P23)
    (h01 : circle_circle_intersection P03 C26 C18)
    (h02 : midpoint P09 P00 P23)
    (h03 : circle_circle_intersection P03 C18 C19)
    (h04 : between P15 P26 P05)
    : length_sum P30 P09 P12 P03 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0700
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0700

theorem v06_sealed_holdout_0701
    (P03 P05 P09 P14 P15 P16 P19 P20 P27 : Point)
    (L00 : Line)
    (C02 C18 C26 C30 : Circle)
    (h00 : equal_length P09 P14 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : angle_bisector_line P19 P20 P16 P27 L00)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : circle_circle_intersection P03 C26 C18)
    : equal_length P09 P14 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0701
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0701

theorem v06_sealed_holdout_0702
    (P02 P03 P08 P10 P12 P13 P16 P17 P19 P22 P23 P24 P25 P27 P29 P30 : Point)
    (L08 L26 : Line)
    (C04 : Circle)
    (h00 : area_eq P30 P17 P22 P02 P12 P23)
    (h01 : area_eq P02 P12 P23 P03 P13 P24)
    (h02 : line_circle_intersection P19 L26 C04)
    (h03 : angle_bisector_line P25 P23 P16 P27 L08)
    (h04 : directed_angle_eq_mod_pi P29 P12 P27 P10 P25 P08)
    : area_eq P30 P17 P22 P03 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0702
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0702

theorem v06_sealed_holdout_0703
    (P01 P04 P05 P08 P11 P14 P15 P16 P18 P21 P22 P24 P27 P28 P29 P30 P31 : Point)
    (L16 : Line)
    (h00 : equal_length P11 P14 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : area_le P30 P27 P24 P21 P18 P15)
    (h03 : area_le P01 P08 P15 P22 P29 P04)
    (h04 : angle_bisector_line P31 P27 P16 P28 L16)
    : equal_length P11 P14 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0703
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0703

theorem v06_sealed_holdout_0704
    (P01 P03 P04 P05 P08 P11 P17 P25 P26 P28 P30 P31 : Point)
    (L08 L24 : Line)
    (h00 : angle_bisector_line P01 P31 P25 P03 L08)
    (h01 : between P05 P04 P03)
    (h02 : midpoint P08 P17 P26)
    (h03 : between P11 P30 P17)
    (h04 : angle_bisector_line P05 P26 P17 P28 L24)
    : angle_bisector P01 P31 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0704
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0704

theorem v06_sealed_holdout_0705
    (P00 P01 P03 P05 P12 P13 P14 P15 P16 P19 P24 P26 P27 P28 P29 : Point)
    (L06 L08 : Line)
    (C02 C22 : Circle)
    (h00 : angle_bisector_line P29 P00 P24 P03 L06)
    (h01 : circle_circle_intersection P19 C22 C02)
    (h02 : between P12 P13 P14)
    (h03 : midpoint P15 P26 P05)
    (h04 : angle_bisector_line P01 P27 P16 P28 L08)
    : angle_bisector P29 P00 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0705
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0705

theorem v06_sealed_holdout_0706
    (P02 P03 P04 P06 P07 P08 P12 P15 P16 P19 P21 P22 P23 P24 P25 P28 P30 P31 : Point)
    (h00 : directed_angle_eq_mod_pi P06 P07 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P08 P16 P24)
    (h02 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    (h03 : between P22 P03 P16)
    (h04 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    : directed_angle_eq_mod_pi P06 P07 P04 P08 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0706
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0706

theorem v06_sealed_holdout_0707
    (P02 P03 P04 P07 P10 P11 P16 P19 P21 P25 P26 P27 P28 P30 P31 : Point)
    (L00 L10 : Line)
    (C08 : Circle)
    (h00 : directed_angle_eq_mod_2pi P27 P11 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : between P26 P31 P04)
    (h03 : line_circle_intersection P19 L10 C08)
    (h04 : angle_bisector_line P03 P27 P16 P28 L00)
    : directed_angle_eq_mod_2pi P27 P11 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0707
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0707

theorem v06_sealed_holdout_0708
    (P04 P06 P07 P08 P09 P15 P16 P19 P21 P23 P24 P25 P31 : Point)
    (L26 : Line)
    (C02 C04 C22 : Circle)
    (h00 : directed_angle_eq_mod_pi P08 P07 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P09 P16 P24)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    (h04 : line_circle_intersection P19 L26 C04)
    : directed_angle_eq_mod_pi P08 P07 P04 P09 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0708
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0708

theorem v06_sealed_holdout_0709
    (P02 P03 P07 P08 P10 P11 P16 P17 P21 P25 P26 P29 P30 : Point)
    (C18 C26 : Circle)
    (h00 : directed_angle_eq_mod_2pi P29 P11 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : between P08 P17 P26)
    (h03 : between P11 P30 P17)
    (h04 : circle_circle_intersection P03 C26 C18)
    : directed_angle_eq_mod_2pi P29 P11 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0709
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0709

theorem v06_sealed_holdout_0710
    (P03 P12 P13 P14 P16 P18 P19 P22 : Point)
    (L02 L10 : Line)
    (C02 C06 C14 C24 C25 : Circle)
    (h00 : circle_through_three_noncollinear_points P18 P22 P16 C25)
    (h01 : between P12 P13 P14)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : line_circle_intersection P03 L02 C06)
    (h04 : line_circle_intersection P19 L10 C24)
    : triangle_pred P18 P22 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0710
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0710

theorem v06_sealed_holdout_0711
    (P00 P01 P03 P06 P07 P19 P21 P22 P25 P28 P29 P30 P31 : Point)
    (C02 C18 C22 C26 : Circle)
    (h00 : equilateral P07 P21 P06)
    (h01 : between P19 P22 P25)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    : triangle_pred P07 P21 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0711
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0711

theorem v06_sealed_holdout_0712
    (P03 P08 P12 P16 P20 P22 P24 P27 P28 P29 : Point)
    (L00 L28 : Line)
    (C07 C10 C18 : Circle)
    (h00 : circle_through_three_noncollinear_points P20 P22 P16 C07)
    (h01 : circle_circle_intersection P03 C10 C18)
    (h02 : between P29 P12 P27)
    (h03 : angle_bisector_line P03 P24 P16 P27 L00)
    (h04 : angle_bisector_line P08 P27 P16 P28 L28)
    : triangle_pred P20 P22 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0712
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0712

theorem v06_sealed_holdout_0713
    (P01 P03 P04 P06 P08 P09 P10 P15 P16 P20 P21 P22 P23 P24 P25 P27 P29 P30 : Point)
    (L12 : Line)
    (h00 : equilateral P09 P22 P06)
    (h01 : area_le P01 P08 P15 P22 P29 P04)
    (h02 : area_le P04 P21 P06 P23 P08 P25)
    (h03 : angle_bisector_line P04 P24 P16 P27 L12)
    (h04 : area_le P10 P15 P20 P25 P30 P03)
    : triangle_pred P09 P22 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0713
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0713

theorem v06_sealed_holdout_0714
    (P00 P03 P06 P08 P10 P16 P17 P21 P22 P26 P27 P28 : Point)
    (L20 L28 : Line)
    (C18 C26 : Circle)
    (h00 : equilateral P10 P22 P06)
    (h01 : between P08 P17 P26)
    (h02 : angle_bisector_line P00 P21 P16 P27 L28)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : angle_bisector_line P10 P27 P16 P28 L20)
    : triangle_pred P10 P22 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0714
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0714

theorem v06_sealed_holdout_0715
    (P05 P07 P11 P12 P13 P14 P15 P16 P17 P18 P19 P20 P21 P26 P27 P28 : Point)
    (L00 : Line)
    (RF58 : Reflection)
    (h00 : between P12 P13 P14)
    (h01 : between P15 P26 P05)
    (h02 : midpoint P18 P07 P28)
    (h03 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    (h04 : angle_bisector_line P11 P27 P16 P28 L00)
    : reflection_image RF58 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0715
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0715

theorem v06_sealed_holdout_0716
    (P00 P10 P11 P16 P18 P19 P21 P22 P25 P27 P28 P29 P30 P31 : Point)
    (L24 : Line)
    (C02 C22 : Circle)
    (HOM51 : Homothety)
    (h00 : between P19 P22 P25)
    (h01 : angle_bisector_line P29 P18 P16 P27 L24)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : midpoint P28 P29 P30)
    (h04 : area_le P31 P10 P21 P00 P11 P22)
    : homothety_image HOM51 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0716
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0716

theorem v06_sealed_holdout_0717
    (P00 P03 P06 P07 P08 P13 P16 P18 P19 P24 P25 P26 P27 : Point)
    (L02 L28 : Line)
    (C02 C06 C22 : Circle)
    (INV48 : Inversion)
    (h00 : line_circle_intersection P03 L02 C22)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : midpoint P00 P25 P18)
    (h03 : angle_bisector_line P08 P24 P16 P27 L28)
    (h04 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    : inversion_image INV48 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0717
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0717

theorem v06_sealed_holdout_0718
    (P04 P06 P08 P10 P14 P15 P16 P19 P20 P21 P23 P25 P26 P27 : Point)
    (L12 L20 : Line)
    (C02 C06 : Circle)
    (SP49 : SpiralSimilarity)
    (h00 : angle_bisector_line P26 P14 P16 P27 L20)
    (h01 : area_le P04 P21 P06 P23 P08 P25)
    (h02 : angle_bisector_line P04 P21 P16 P27 L12)
    (h03 : midpoint P10 P15 P20)
    (h04 : circle_circle_intersection P19 C06 C02)
    : spiral_similarity_center SP49 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0718
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0718

theorem v06_sealed_holdout_0719
    (P03 P05 P07 P08 P09 P19 P20 P22 P24 P28 P31 : Point)
    (C02 C22 : Circle)
    (h00 : P03 = P08)
    (h01 : P22 = P19)
    (h02 : P28 = P31)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : area_le P20 P05 P22 P07 P24 P09)
    : rotation_preserves_collinear P03 P22 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0719
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0719

theorem v06_sealed_holdout_0720
    (P01 P06 P07 P08 P10 P12 P17 P18 P19 P24 P27 P28 : Point)
    (L10 L26 : Line)
    (C24 C27 C28 : Circle)
    (h00 : circle_with_center_through_point P12 P08 C27)
    (h01 : area_le P18 P07 P28 P17 P06 P27)
    (h02 : line_circle_intersection P19 L10 C24)
    (h03 : midpoint P24 P01 P10)
    (h04 : line_circle_intersection P19 L26 C28)
    : on_circle P08 C27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0720
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0720

theorem v06_sealed_holdout_0721
    (P03 P10 P17 P19 P22 P26 P28 P29 P30 : Point)
    (L02 L04 L21 : Line)
    (C02 C06 C14 C19 : Circle)
    (h00 : line_circle_intersection P10 L21 C19)
    (h01 : midpoint P28 P29 P30)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : line_circle_intersection P03 L02 C06)
    (h04 : angle_bisector_line P22 P26 P17 P28 L04)
    : on_circle P10 C19 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0721
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0721

theorem v06_sealed_holdout_0722
    (P00 P03 P06 P07 P08 P09 P12 P15 P17 P18 P23 P26 P28 : Point)
    (L02 L16 : Line)
    (C20 C30 : Circle)
    (h00 : chord P07 P08 C20)
    (h01 : directed_angle_eq_mod_pi P03 P06 P09 P12 P15 P18)
    (h02 : line_circle_intersection P03 L02 C30)
    (h03 : between P09 P00 P23)
    (h04 : angle_bisector_line P23 P26 P17 P28 L16)
    : on_circle P07 C20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0722
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0722

theorem v06_sealed_holdout_0723
    (P02 P03 P09 P10 P11 P13 P16 P18 P22 P23 P24 P28 P29 : Point)
    (L07 L28 : Line)
    (C04 : Circle)
    (h00 : line_circle_intersection P29 L07 C04)
    (h01 : midpoint P13 P28 P11)
    (h02 : midpoint P16 P09 P02)
    (h03 : angle_bisector_line P24 P22 P18 P28 L28)
    (h04 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    : on_line P29 L07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0723
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0723

theorem v06_sealed_holdout_0724
    (P04 P05 P07 P09 P14 P18 P19 P20 P22 P23 P24 P26 P31 : Point)
    (L07 : Line)
    (C02 C06 C14 : Circle)
    (h00 : altitude P18 P24 P14 P23 L07)
    (h01 : area_le P20 P05 P22 P07 P24 P09)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : midpoint P26 P31 P04)
    (h04 : circle_circle_intersection P19 C06 C02)
    : on_line P14 L07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0724
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0724

theorem v06_sealed_holdout_0725
    (P01 P08 P11 P13 P14 P15 P17 P18 P19 P21 P23 P24 P25 P27 P28 P30 : Point)
    (L00 L01 : Line)
    (C02 C30 : Circle)
    (h00 : altitude P14 P25 P13 P23 L01)
    (h01 : angle_bisector_line P11 P17 P18 P28 L00)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : area_le P30 P27 P24 P21 P18 P15)
    (h04 : between P01 P08 P15)
    : on_line P13 L01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0725
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0725

theorem v06_sealed_holdout_0726
    (P03 P08 P17 P18 P19 P20 P26 P28 P29 : Point)
    (L08 L16 : Line)
    (C02 C06 C14 : Circle)
    (h00 : angle_bisector_line P03 P28 P19 P29 L16)
    (h01 : circle_circle_intersection P19 C14 C02)
    (h02 : angle_bisector_line P17 P20 P18 P28 L08)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : between P08 P17 P26)
    : on_line P03 L16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0726
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0726

theorem v06_sealed_holdout_0727
    (P03 P05 P15 P19 P26 P28 : Point)
    (L02 L18 : Line)
    (C02 C18 C19 C22 C28 C30 : Circle)
    (h00 : line_circle_intersection P28 L18 C28)
    (h01 : line_circle_intersection P03 L02 C30)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : circle_circle_intersection P03 C18 C19)
    (h04 : midpoint P15 P26 P05)
    : on_line P28 L18 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0727
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0727

theorem v06_sealed_holdout_0728
    (P01 P03 P09 P11 P13 P16 P18 P19 P22 P24 P26 P28 : Point)
    (L26 : Line)
    (C02 C12 C18 : Circle)
    (h00 : equilateral P09 P18 P01)
    (h01 : area_le P13 P28 P11 P26 P09 P24)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : line_circle_intersection P19 L26 C12)
    (h04 : between P22 P03 P16)
    : equal_length P09 P18 P18 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0728
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0728

theorem v06_sealed_holdout_0729
    (P00 P03 P04 P05 P06 P08 P09 P13 P14 P17 P18 P19 P20 P23 P24 P26 P30 P31 : Point)
    (C18 C19 : Circle)
    (h00 : equilateral P05 P19 P00)
    (h01 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    (h02 : circle_circle_intersection P03 C18 C19)
    (h03 : area_le P23 P18 P13 P08 P03 P30)
    (h04 : area_le P26 P31 P04 P09 P14 P19)
    : equal_length P05 P19 P19 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0729
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0729

theorem v06_sealed_holdout_0730
    (P01 P04 P07 P09 P10 P11 P14 P16 P18 P19 P20 P23 P24 P26 P27 P30 : Point)
    (L00 L10 : Line)
    (C00 : Circle)
    (h00 : length_sum P10 P04 P30 P09 P16 P23)
    (h01 : angle_bisector_line P11 P18 P16 P27 L00)
    (h02 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    (h03 : between P30 P27 P24)
    (h04 : line_circle_intersection P19 L10 C00)
    : length_sum P30 P09 P10 P04 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0730
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0730

theorem v06_sealed_holdout_0731
    (P01 P02 P03 P05 P07 P08 P11 P12 P15 P16 P17 P19 P21 P22 P23 P26 P27 : Point)
    (L10 : Line)
    (C24 : Circle)
    (h00 : equal_length P07 P15 P16 P27)
    (h01 : equal_length P16 P27 P05 P17)
    (h02 : area_le P02 P23 P12 P01 P22 P11)
    (h03 : line_circle_intersection P19 L10 C24)
    (h04 : directed_angle_eq_mod_pi P08 P17 P26 P03 P12 P21)
    : equal_length P07 P15 P05 P17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0731
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0731

theorem v06_sealed_holdout_0732
    (P00 P02 P03 P05 P09 P12 P13 P14 P15 P16 P17 P18 P19 P22 P23 P24 P28 : Point)
    (L26 : Line)
    (C20 : Circle)
    (h00 : area_eq P28 P18 P22 P02 P12 P23)
    (h01 : area_eq P02 P12 P23 P03 P13 P24)
    (h02 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h03 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h04 : line_circle_intersection P19 L26 C20)
    : area_eq P28 P18 P22 P03 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0732
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0732

theorem v06_sealed_holdout_0733
    (P02 P03 P05 P09 P13 P15 P16 P17 P20 P24 P25 P27 : Point)
    (L28 : Line)
    (C18 C26 : Circle)
    (h00 : equal_length P09 P15 P16 P27)
    (h01 : equal_length P16 P27 P05 P17)
    (h02 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    (h03 : angle_bisector_line P24 P25 P16 P27 L28)
    (h04 : circle_circle_intersection P03 C26 C18)
    : equal_length P09 P15 P05 P17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0733
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0733

theorem v06_sealed_holdout_0734
    (P00 P03 P13 P18 P19 P23 P25 P31 : Point)
    (L02 L10 L18 : Line)
    (C02 C06 C22 C26 : Circle)
    (h00 : angle_bisector_line P31 P00 P25 P03 L10)
    (h01 : midpoint P23 P18 P13)
    (h02 : line_circle_intersection P03 L02 C22)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : line_circle_intersection P03 L18 C26)
    : angle_bisector P31 P00 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0734
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0734

theorem v06_sealed_holdout_0735
    (P01 P03 P04 P06 P14 P19 P21 P24 P27 P30 : Point)
    (L08 : Line)
    (C02 C22 : Circle)
    (h00 : angle_bisector_line P27 P01 P24 P03 L08)
    (h01 : midpoint P27 P14 P01)
    (h02 : between P30 P27 P24)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : midpoint P04 P21 P06)
    : angle_bisector P27 P01 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0735
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0735

theorem v06_sealed_holdout_0736
    (P04 P05 P07 P08 P11 P15 P16 P17 P21 P22 P23 P24 P26 P27 P30 P31 : Point)
    (L04 : Line)
    (h00 : directed_angle_eq_mod_pi P04 P08 P05 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : angle_bisector_line P22 P21 P16 P27 L04)
    (h03 : between P08 P17 P26)
    (h04 : between P11 P30 P17)
    : directed_angle_eq_mod_pi P04 P08 P05 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0736
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0736

theorem v06_sealed_holdout_0737
    (P02 P03 P05 P06 P07 P10 P11 P12 P13 P14 P15 P16 P17 P21 P25 P26 P27 P30 : Point)
    (C10 C18 : Circle)
    (h00 : directed_angle_eq_mod_2pi P25 P11 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P26 P02)
    (h02 : area_le P12 P13 P14 P15 P16 P17)
    (h03 : directed_angle_eq_mod_pi P15 P26 P05 P16 P27 P06)
    (h04 : circle_circle_intersection P03 C10 C18)
    : directed_angle_eq_mod_2pi P25 P11 P10 P16 P26 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0737
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0737

theorem v06_sealed_holdout_0738
    (P03 P04 P06 P07 P08 P10 P15 P16 P21 P22 P23 P24 P25 P27 P29 P31 : Point)
    (L28 : Line)
    (h00 : directed_angle_eq_mod_pi P06 P08 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : angle_bisector_line P24 P21 P16 P27 L28)
    (h03 : area_le P22 P03 P16 P29 P10 P23)
    (h04 : midpoint P25 P16 P07)
    : directed_angle_eq_mod_pi P06 P08 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0738
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0738

theorem v06_sealed_holdout_0739
    (P02 P03 P04 P07 P10 P12 P16 P21 P25 P26 P27 P28 P30 P31 : Point)
    (L00 L04 : Line)
    (h00 : directed_angle_eq_mod_2pi P27 P12 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : between P26 P31 P04)
    (h03 : angle_bisector_line P30 P25 P16 P27 L04)
    (h04 : angle_bisector_line P03 P28 P16 P27 L00)
    : directed_angle_eq_mod_2pi P27 P12 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0739
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0739

theorem v06_sealed_holdout_0740
    (P02 P03 P07 P14 P16 P17 P19 P23 P24 P25 P27 P29 P31 : Point)
    (L10 L16 : Line)
    (C00 C11 C18 C26 : Circle)
    (h00 : circle_through_three_noncollinear_points P16 P23 P17 C11)
    (h01 : circle_circle_intersection P03 C26 C18)
    (h02 : line_circle_intersection P19 L10 C00)
    (h03 : angle_bisector_line P31 P25 P16 P27 L16)
    (h04 : area_le P07 P02 P29 P24 P19 P14)
    : triangle_pred P16 P23 P17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0740
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0740

theorem v06_sealed_holdout_0741
    (P00 P01 P02 P03 P04 P05 P06 P08 P11 P12 P14 P17 P21 P22 P26 P30 : Point)
    (h00 : equilateral P05 P22 P06)
    (h01 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    (h02 : directed_angle_eq_mod_pi P08 P17 P26 P03 P12 P21)
    (h03 : midpoint P11 P30 P17)
    (h04 : between P14 P11 P08)
    : triangle_pred P05 P22 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0741
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0741

theorem v06_sealed_holdout_0742
    (P03 P05 P06 P07 P15 P16 P18 P23 P26 P27 P28 : Point)
    (L04 L18 : Line)
    (C02 C25 : Circle)
    (h00 : circle_through_three_noncollinear_points P18 P23 P16 C25)
    (h01 : line_circle_intersection P03 L18 C02)
    (h02 : directed_angle_eq_mod_pi P15 P26 P05 P16 P27 P06)
    (h03 : between P18 P07 P28)
    (h04 : angle_bisector_line P06 P28 P16 P27 L04)
    : triangle_pred P18 P23 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0742
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0742

theorem v06_sealed_holdout_0743
    (P03 P06 P07 P12 P16 P19 P21 P22 P25 P30 : Point)
    (L02 : Line)
    (C18 C19 C30 : Circle)
    (h00 : equilateral P07 P22 P06)
    (h01 : midpoint P19 P22 P25)
    (h02 : line_circle_intersection P03 L02 C30)
    (h03 : area_le P25 P16 P07 P30 P21 P12)
    (h04 : circle_circle_intersection P03 C18 C19)
    : triangle_pred P07 P22 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0743
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0743

theorem v06_sealed_holdout_0744
    (P00 P03 P04 P06 P08 P09 P11 P12 P15 P16 P18 P22 P23 P25 P26 P27 P29 P30 P31 : Point)
    (L04 : Line)
    (h00 : equilateral P08 P23 P06)
    (h01 : between P26 P31 P04)
    (h02 : angle_bisector_line P30 P22 P16 P27 L04)
    (h03 : area_le P00 P25 P18 P11 P04 P29)
    (h04 : area_le P03 P06 P09 P12 P15 P18)
    : triangle_pred P08 P23 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0744
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0744

theorem v06_sealed_holdout_0745
    (P01 P03 P04 P06 P08 P15 P19 P21 P24 P27 P30 : Point)
    (L02 L26 : Line)
    (C04 C22 : Circle)
    (RF12 : Reflection)
    (h00 : midpoint P30 P27 P24)
    (h01 : midpoint P01 P08 P15)
    (h02 : midpoint P04 P21 P06)
    (h03 : line_circle_intersection P19 L26 C04)
    (h04 : line_circle_intersection P03 L02 C22)
    : reflection_image RF12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0745
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0745

theorem v06_sealed_holdout_0746
    (P00 P03 P04 P05 P08 P10 P12 P16 P17 P21 P22 P26 P27 P28 : Point)
    (L20 L28 : Line)
    (C18 C26 : Circle)
    (HOM01 : Homothety)
    (h00 : between P05 P04 P03)
    (h01 : directed_angle_eq_mod_pi P08 P17 P26 P03 P12 P21)
    (h02 : angle_bisector_line P00 P22 P16 P27 L28)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : angle_bisector_line P10 P28 P16 P27 L20)
    : homothety_image HOM01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0746
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0746

theorem v06_sealed_holdout_0747
    (P01 P03 P05 P06 P10 P12 P13 P14 P15 P16 P19 P20 P21 P24 P26 P27 P28 : Point)
    (C10 C18 : Circle)
    (INV58 : Inversion)
    (h00 : midpoint P12 P13 P14)
    (h01 : directed_angle_eq_mod_pi P15 P26 P05 P16 P27 P06)
    (h02 : circle_circle_intersection P03 C10 C18)
    (h03 : midpoint P21 P20 P19)
    (h04 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    : inversion_image INV58 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0747
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0747

theorem v06_sealed_holdout_0748
    (P02 P03 P07 P10 P16 P19 P21 P22 P25 P27 P28 P31 : Point)
    (L16 L20 : Line)
    (SP55 : SpiralSimilarity)
    (h00 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    (h01 : between P22 P03 P16)
    (h02 : angle_bisector_line P02 P22 P16 P27 L20)
    (h03 : angle_bisector_line P07 P25 P16 P27 L16)
    (h04 : midpoint P31 P10 P21)
    : spiral_similarity_center SP55 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0748
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0748

theorem v06_sealed_holdout_0749
    (P00 P01 P06 P08 P19 P22 P28 P31 : Point)
    (L26 : Line)
    (C12 : Circle)
    (h00 : P01 = P08)
    (h01 : P22 = P19)
    (h02 : P28 = P31)
    (h03 : line_circle_intersection P19 L26 C12)
    (h04 : midpoint P06 P19 P00)
    : rotation_preserves_collinear P01 P22 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0749
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0749

theorem v06_sealed_holdout_0750
    (P03 P10 P11 P15 P19 P20 P25 P30 P31 : Point)
    (L10 : Line)
    (C01 C02 C08 C14 C18 : Circle)
    (h00 : circle_through_three_noncollinear_points P03 P11 P31 C01)
    (h01 : circle_circle_intersection P19 C14 C02)
    (h02 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    (h03 : line_circle_intersection P19 L10 C08)
    (h04 : circle_circle_intersection P03 C02 C18)
    : on_circle P03 C01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0750
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0750

theorem v06_sealed_holdout_0751
    (P02 P05 P08 P11 P14 P15 P17 P19 P24 P28 P31 : Point)
    (L16 L21 L26 : Line)
    (C01 C04 : Circle)
    (h00 : line_circle_intersection P08 L21 C01)
    (h01 : directed_angle_eq_mod_pi P14 P11 P08 P05 P02 P31)
    (h02 : between P17 P24 P31)
    (h03 : angle_bisector_line P15 P24 P17 P28 L16)
    (h04 : line_circle_intersection P19 L26 C04)
    : on_circle P08 C01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0751
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0751

theorem v06_sealed_holdout_0752
    (P01 P05 P08 P10 P19 P24 P27 P30 : Point)
    (C02 C06 C28 C30 : Circle)
    (h00 : chord P05 P08 C28)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : midpoint P24 P01 P10)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : between P30 P27 P24)
    : on_circle P05 C28 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0752
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0752

theorem v06_sealed_holdout_0753
    (P00 P01 P02 P03 P04 P05 P10 P11 P12 P18 P21 P22 P23 P26 P27 P28 P31 : Point)
    (L00 L09 : Line)
    (C20 : Circle)
    (h00 : line_circle_intersection P27 L09 C20)
    (h01 : area_le P31 P10 P21 P00 P11 P22)
    (h02 : area_le P02 P23 P12 P01 P22 P11)
    (h03 : between P05 P04 P03)
    (h04 : angle_bisector_line P27 P26 P18 P28 L00)
    : on_line P27 L09 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0753
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0753

theorem v06_sealed_holdout_0754
    (P03 P05 P06 P12 P13 P14 P15 P16 P17 P19 P23 P25 P26 P27 : Point)
    (L10 L13 : Line)
    (C16 C18 C26 : Circle)
    (h00 : altitude P16 P25 P14 P23 L13)
    (h01 : circle_circle_intersection P03 C26 C18)
    (h02 : line_circle_intersection P19 L10 C16)
    (h03 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h04 : area_le P15 P26 P05 P16 P27 P06)
    : on_line P14 L13 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0754
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0754

theorem v06_sealed_holdout_0755
    (P02 P09 P10 P11 P12 P13 P15 P16 P19 P20 P23 P26 P28 : Point)
    (L07 L26 : Line)
    (C12 : Circle)
    (h00 : altitude P12 P26 P13 P23 L07)
    (h01 : midpoint P10 P15 P20)
    (h02 : between P13 P28 P11)
    (h03 : midpoint P16 P09 P02)
    (h04 : line_circle_intersection P19 L26 C12)
    : on_line P13 L07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0755
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0755

theorem v06_sealed_holdout_0756
    (P01 P04 P06 P09 P13 P14 P15 P17 P19 P20 P21 P24 P26 P28 P29 P30 P31 : Point)
    (L16 L20 L26 : Line)
    (C04 : Circle)
    (h00 : angle_bisector_line P01 P29 P19 P30 L20)
    (h01 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    (h02 : angle_bisector_line P15 P21 P17 P28 L16)
    (h03 : line_circle_intersection P19 L26 C04)
    (h04 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    : on_line P01 L20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0756
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0756

theorem v06_sealed_holdout_0757
    (P01 P07 P08 P10 P14 P15 P18 P20 P21 P24 P26 P27 P30 : Point)
    (L20 : Line)
    (C12 : Circle)
    (h00 : line_circle_intersection P26 L20 C12)
    (h01 : between P24 P01 P10)
    (h02 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    (h03 : area_le P30 P27 P24 P21 P18 P15)
    (h04 : between P01 P08 P15)
    : on_line P26 L20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0757
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0757

theorem v06_sealed_holdout_0758
    (P01 P02 P07 P08 P12 P17 P18 P19 P23 P26 P28 : Point)
    (L10 L12 : Line)
    (C24 : Circle)
    (h00 : equilateral P07 P19 P01)
    (h01 : angle_bisector_line P12 P18 P17 P28 L12)
    (h02 : midpoint P02 P23 P12)
    (h03 : line_circle_intersection P19 L10 C24)
    (h04 : midpoint P08 P17 P26)
    : equal_length P07 P19 P19 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0758
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0758

theorem v06_sealed_holdout_0759
    (P00 P03 P06 P09 P12 P13 P14 P16 P18 P19 P25 P27 : Point)
    (L20 : Line)
    (h00 : equilateral P03 P19 P00)
    (h01 : between P03 P06 P09)
    (h02 : midpoint P06 P19 P00)
    (h03 : angle_bisector_line P18 P25 P16 P27 L20)
    (h04 : between P12 P13 P14)
    : equal_length P03 P19 P19 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0759
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0759

theorem v06_sealed_holdout_0760
    (P02 P05 P08 P09 P10 P11 P13 P15 P16 P20 P23 P24 P27 P28 P30 : Point)
    (L28 : Line)
    (h00 : length_sum P08 P05 P30 P09 P16 P23)
    (h01 : between P10 P15 P20)
    (h02 : midpoint P13 P28 P11)
    (h03 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    (h04 : angle_bisector_line P24 P28 P16 P27 L28)
    : length_sum P30 P09 P08 P05 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0760
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0760

theorem v06_sealed_holdout_0761
    (P03 P04 P05 P06 P08 P13 P15 P16 P17 P18 P20 P22 P23 P26 P27 P30 P31 : Point)
    (h00 : equal_length P05 P16 P17 P27)
    (h01 : equal_length P17 P27 P06 P15)
    (h02 : midpoint P20 P05 P22)
    (h03 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    (h04 : between P26 P31 P04)
    : equal_length P05 P16 P06 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0761
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0761

theorem v06_sealed_holdout_0762
    (P01 P02 P03 P08 P12 P13 P15 P18 P19 P21 P22 P23 P24 P26 P27 P30 : Point)
    (L26 : Line)
    (C28 : Circle)
    (h00 : area_eq P26 P19 P22 P02 P12 P23)
    (h01 : area_eq P02 P12 P23 P03 P13 P24)
    (h02 : line_circle_intersection P19 L26 C28)
    (h03 : area_le P30 P27 P24 P21 P18 P15)
    (h04 : between P01 P08 P15)
    : area_eq P26 P19 P22 P03 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0762
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0762

theorem v06_sealed_holdout_0763
    (P03 P05 P07 P08 P12 P15 P16 P17 P19 P21 P26 P27 : Point)
    (C02 C06 C10 C18 : Circle)
    (h00 : equal_length P07 P16 P17 P27)
    (h01 : equal_length P17 P27 P05 P15)
    (h02 : circle_circle_intersection P03 C10 C18)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : area_le P08 P17 P26 P03 P12 P21)
    : equal_length P07 P16 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0763
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0763

theorem v06_sealed_holdout_0764
    (P00 P01 P03 P05 P06 P07 P09 P12 P13 P14 P15 P16 P17 P18 P23 P25 P26 P27 P28 P29 : Point)
    (L12 : Line)
    (h00 : angle_bisector_line P29 P01 P25 P03 L12)
    (h01 : midpoint P09 P00 P23)
    (h02 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h03 : directed_angle_eq_mod_pi P15 P26 P05 P16 P27 P06)
    (h04 : area_le P18 P07 P28 P17 P06 P27)
    : angle_bisector P29 P01 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0764
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0764

theorem v06_sealed_holdout_0765
    (P02 P03 P09 P10 P11 P13 P16 P20 P22 P23 P24 P25 P26 P27 P28 P29 : Point)
    (L10 L28 : Line)
    (h00 : angle_bisector_line P25 P02 P24 P03 L10)
    (h01 : area_le P13 P28 P11 P26 P09 P24)
    (h02 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    (h03 : angle_bisector_line P24 P25 P16 P27 L28)
    (h04 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    : angle_bisector P25 P02 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0765
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0765

theorem v06_sealed_holdout_0766
    (P02 P04 P07 P09 P14 P15 P16 P19 P23 P24 P26 P27 P29 P30 P31 : Point)
    (L04 : Line)
    (C02 C14 : Circle)
    (h00 : directed_angle_eq_mod_pi P02 P09 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : area_le P26 P31 P04 P09 P14 P19)
    (h04 : angle_bisector_line P30 P29 P16 P27 L04)
    : directed_angle_eq_mod_pi P02 P09 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0766
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0766

theorem v06_sealed_holdout_0767
    (P02 P03 P04 P06 P07 P08 P10 P12 P16 P19 P21 P23 P25 P30 : Point)
    (L02 L10 : Line)
    (C00 C14 : Circle)
    (h00 : directed_angle_eq_mod_2pi P23 P12 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : line_circle_intersection P03 L02 C14)
    (h03 : line_circle_intersection P19 L10 C00)
    (h04 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    : directed_angle_eq_mod_2pi P23 P12 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0767
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0767

theorem v06_sealed_holdout_0768
    (P00 P01 P02 P03 P04 P05 P07 P09 P15 P16 P19 P23 P24 P25 P27 P28 P31 : Point)
    (L00 L26 : Line)
    (C28 : Circle)
    (h00 : directed_angle_eq_mod_pi P04 P09 P05 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : area_le P05 P04 P03 P02 P01 P00)
    (h03 : angle_bisector_line P27 P25 P16 P28 L00)
    (h04 : line_circle_intersection P19 L26 C28)
    : directed_angle_eq_mod_pi P04 P09 P05 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0768
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0768

theorem v06_sealed_holdout_0769
    (P02 P03 P07 P10 P12 P13 P14 P15 P16 P17 P19 P21 P25 P26 P30 : Point)
    (C02 C10 C14 C18 : Circle)
    (h00 : directed_angle_eq_mod_2pi P25 P12 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P26 P02)
    (h02 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h03 : circle_circle_intersection P19 C14 C02)
    (h04 : circle_circle_intersection P03 C10 C18)
    : directed_angle_eq_mod_2pi P25 P12 P10 P16 P26 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0769
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0769

theorem v06_sealed_holdout_0770
    (P03 P07 P12 P14 P16 P19 P20 P21 P22 P24 P25 P27 P30 : Point)
    (L00 : Line)
    (C02 C29 C30 : Circle)
    (h00 : circle_through_three_noncollinear_points P14 P24 P16 C29)
    (h01 : angle_bisector_line P19 P20 P16 P27 L00)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : midpoint P22 P03 P16)
    (h04 : area_le P25 P16 P07 P30 P21 P12)
    : triangle_pred P14 P24 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0770
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0770

theorem v06_sealed_holdout_0771
    (P00 P03 P04 P06 P08 P10 P11 P12 P13 P18 P23 P25 P26 P27 P29 P30 P31 : Point)
    (h00 : equilateral P03 P23 P06)
    (h01 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    (h02 : between P26 P31 P04)
    (h03 : area_le P29 P12 P27 P10 P25 P08)
    (h04 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    : triangle_pred P03 P23 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0771
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0771

theorem v06_sealed_holdout_0772
    (P01 P02 P03 P04 P07 P08 P14 P15 P16 P17 P19 P22 P24 P26 P27 P29 P31 : Point)
    (L02 L16 : Line)
    (C11 C14 : Circle)
    (h00 : circle_through_three_noncollinear_points P16 P24 P17 C11)
    (h01 : line_circle_intersection P03 L02 C14)
    (h02 : area_le P01 P08 P15 P22 P29 P04)
    (h03 : angle_bisector_line P31 P26 P16 P27 L16)
    (h04 : directed_angle_eq_mod_pi P07 P02 P29 P24 P19 P14)
    : triangle_pred P16 P24 P17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0772
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0772

theorem v06_sealed_holdout_0773
    (P00 P01 P02 P03 P04 P05 P06 P11 P17 P23 P30 : Point)
    (L02 L18 : Line)
    (C10 C14 : Circle)
    (h00 : equilateral P05 P23 P06)
    (h01 : area_le P05 P04 P03 P02 P01 P00)
    (h02 : line_circle_intersection P03 L18 C10)
    (h03 : between P11 P30 P17)
    (h04 : line_circle_intersection P03 L02 C14)
    : triangle_pred P05 P23 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0773
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0773

theorem v06_sealed_holdout_0774
    (P06 P07 P12 P13 P14 P15 P16 P17 P18 P19 P20 P21 P22 P23 P27 P28 : Point)
    (L12 : Line)
    (h00 : equilateral P06 P23 P07)
    (h01 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h02 : angle_bisector_line P28 P22 P16 P27 L12)
    (h03 : midpoint P18 P07 P28)
    (h04 : midpoint P21 P20 P19)
    : triangle_pred P06 P23 P07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0774
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0774

theorem v06_sealed_holdout_0775
    (P00 P01 P02 P03 P09 P16 P19 P22 P25 P28 P29 P30 P31 : Point)
    (L10 : Line)
    (C16 : Circle)
    (RF30 : Reflection)
    (h00 : between P16 P09 P02)
    (h01 : midpoint P19 P22 P25)
    (h02 : between P22 P03 P16)
    (h03 : line_circle_intersection P19 L10 C16)
    (h04 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    : reflection_image RF30 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0775
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0775

theorem v06_sealed_holdout_0776
    (P03 P04 P06 P08 P09 P13 P16 P18 P19 P23 P26 P27 P30 P31 : Point)
    (L00 : Line)
    (C02 C06 : Circle)
    (HOM15 : Homothety)
    (h00 : area_le P23 P18 P13 P08 P03 P30)
    (h01 : midpoint P26 P31 P04)
    (h02 : circle_circle_intersection P19 C06 C02)
    (h03 : angle_bisector_line P03 P26 P16 P27 L00)
    (h04 : midpoint P03 P06 P09)
    : homothety_image HOM15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0776
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0776

theorem v06_sealed_holdout_0777
    (P01 P03 P04 P06 P08 P15 P16 P17 P19 P21 P22 P27 P29 : Point)
    (L24 L26 : Line)
    (C04 C10 C18 : Circle)
    (INV04 : Inversion)
    (h00 : angle_bisector_line P21 P16 P17 P27 L24)
    (h01 : area_le P01 P08 P15 P22 P29 P04)
    (h02 : between P04 P21 P06)
    (h03 : line_circle_intersection P19 L26 C04)
    (h04 : circle_circle_intersection P03 C10 C18)
    : inversion_image INV04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0777
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0777

theorem v06_sealed_holdout_0778
    (P03 P04 P05 P06 P10 P11 P13 P16 P17 P20 P22 P23 P24 P26 P27 P30 P31 : Point)
    (L04 L18 L24 : Line)
    (C10 : Circle)
    (SP61 : SpiralSimilarity)
    (h00 : angle_bisector_line P22 P16 P17 P27 L04)
    (h01 : line_circle_intersection P03 L18 C10)
    (h02 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h03 : angle_bisector_line P05 P26 P16 P27 L24)
    (h04 : area_le P17 P24 P31 P06 P13 P20)
    : spiral_similarity_center SP61 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0778
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0778

theorem v06_sealed_holdout_0779
    (P00 P01 P05 P08 P10 P19 P20 P21 P23 P24 P28 P31 : Point)
    (h00 : P31 = P08)
    (h01 : P23 = P19)
    (h02 : P28 = P00)
    (h03 : between P21 P20 P19)
    (h04 : area_le P24 P01 P10 P19 P28 P05)
    : rotation_preserves_collinear P31 P23 P28 P08 P19 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0779
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0779

theorem v06_sealed_holdout_0780
    (P00 P03 P08 P10 P11 P19 P21 P22 P31 : Point)
    (L10 L18 : Line)
    (C02 C03 C16 C18 C26 : Circle)
    (h00 : circle_with_center_through_point P08 P10 C03)
    (h01 : circle_circle_intersection P03 C26 C18)
    (h02 : line_circle_intersection P19 L10 C16)
    (h03 : line_circle_intersection P03 L18 C02)
    (h04 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    : on_circle P10 C03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0780
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0780

theorem v06_sealed_holdout_0781
    (P00 P03 P06 P09 P12 P15 P17 P18 P19 P23 P28 : Point)
    (L00 L02 L21 : Line)
    (C15 C30 : Circle)
    (h00 : line_circle_intersection P06 L21 C15)
    (h01 : angle_bisector_line P03 P19 P17 P28 L00)
    (h02 : directed_angle_eq_mod_pi P03 P06 P09 P12 P15 P18)
    (h03 : line_circle_intersection P03 L02 C30)
    (h04 : between P09 P00 P23)
    : on_circle P06 C15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0781
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0781

theorem v06_sealed_holdout_0782
    (P02 P03 P07 P09 P10 P11 P13 P15 P17 P19 P20 P28 P29 : Point)
    (L00 : Line)
    (C04 : Circle)
    (h00 : chord P03 P09 C04)
    (h01 : between P07 P02 P29)
    (h02 : midpoint P10 P15 P20)
    (h03 : midpoint P13 P28 P11)
    (h04 : angle_bisector_line P19 P28 P17 P29 L00)
    : on_circle P03 C04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0782
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0782

theorem v06_sealed_holdout_0783
    (P03 P05 P06 P08 P13 P17 P18 P20 P22 P23 P24 P25 P30 P31 : Point)
    (L02 L11 : Line)
    (C04 C22 : Circle)
    (h00 : line_circle_intersection P25 L11 C04)
    (h01 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    (h02 : between P20 P05 P22)
    (h03 : area_le P23 P18 P13 P08 P03 P30)
    (h04 : line_circle_intersection P03 L02 C22)
    : on_line P25 L11 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0783
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0783

theorem v06_sealed_holdout_0784
    (P01 P03 P04 P08 P11 P14 P15 P18 P19 P22 P23 P26 P28 P29 : Point)
    (L00 L19 : Line)
    (C02 C18 C26 C30 : Circle)
    (h00 : altitude P14 P26 P15 P23 L19)
    (h01 : angle_bisector_line P11 P18 P19 P28 L00)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : area_le P01 P08 P15 P22 P29 P04)
    : on_line P15 L19 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0784
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0784

theorem v06_sealed_holdout_0785
    (P00 P01 P02 P10 P11 P12 P13 P19 P21 P22 P23 P26 P28 P29 P30 P31 : Point)
    (L10 L13 : Line)
    (C24 : Circle)
    (h00 : altitude P10 P26 P13 P23 L13)
    (h01 : area_le P28 P29 P30 P31 P00 P01)
    (h02 : midpoint P31 P10 P21)
    (h03 : directed_angle_eq_mod_pi P02 P23 P12 P01 P22 P11)
    (h04 : line_circle_intersection P19 L10 C24)
    : on_line P13 L13 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0785
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0785

theorem v06_sealed_holdout_0786
    (P00 P04 P05 P06 P08 P09 P11 P12 P14 P16 P18 P19 P23 P25 P27 P28 P29 : Point)
    (L07 L28 : Line)
    (h00 : altitude P06 P27 P12 P23 L07)
    (h01 : area_le P00 P25 P18 P11 P04 P29)
    (h02 : angle_bisector_line P08 P23 P16 P27 L28)
    (h03 : between P06 P19 P00)
    (h04 : area_le P09 P00 P23 P14 P05 P28)
    : on_line P12 L07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0786
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0786

theorem v06_sealed_holdout_0787
    (P02 P09 P10 P13 P14 P15 P16 P17 P19 P20 P22 P24 P25 P27 P28 P31 : Point)
    (L04 L22 : Line)
    (C28 : Circle)
    (h00 : line_circle_intersection P24 L22 C28)
    (h01 : midpoint P10 P15 P20)
    (h02 : angle_bisector_line P14 P22 P17 P28 L04)
    (h03 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    (h04 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    : on_line P24 L22 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0787
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0787

theorem v06_sealed_holdout_0788
    (P01 P03 P04 P05 P07 P08 P09 P13 P18 P19 P20 P22 P23 P24 P26 P30 P31 : Point)
    (L10 : Line)
    (C00 : Circle)
    (h00 : equilateral P05 P20 P01)
    (h01 : line_circle_intersection P19 L10 C00)
    (h02 : directed_angle_eq_mod_pi P20 P05 P22 P07 P24 P09)
    (h03 : area_le P23 P18 P13 P08 P03 P30)
    (h04 : midpoint P26 P31 P04)
    : equal_length P05 P20 P20 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0788
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0788

theorem v06_sealed_holdout_0789
    (P00 P01 P06 P11 P14 P16 P20 P21 P23 P27 P29 : Point)
    (L00 L04 L24 : Line)
    (h00 : equilateral P01 P20 P00)
    (h01 : angle_bisector_line P06 P20 P16 P27 L04)
    (h02 : angle_bisector_line P11 P23 P16 P27 L00)
    (h03 : between P27 P14 P01)
    (h04 : angle_bisector_line P21 P29 P16 P27 L24)
    : equal_length P01 P20 P20 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0789
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0789

theorem v06_sealed_holdout_0790
    (P06 P07 P09 P16 P17 P19 P20 P23 P26 P27 P30 : Point)
    (L08 L10 L16 : Line)
    (C02 C14 C24 : Circle)
    (h00 : length_sum P06 P07 P30 P09 P16 P23)
    (h01 : angle_bisector_line P07 P20 P16 P27 L16)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : angle_bisector_line P17 P26 P16 P27 L08)
    (h04 : line_circle_intersection P19 L10 C24)
    : length_sum P30 P09 P06 P07 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0790
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0790

theorem v06_sealed_holdout_0791
    (P00 P03 P05 P06 P09 P12 P13 P14 P15 P16 P17 P19 P23 P27 P28 : Point)
    (h00 : equal_length P03 P17 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : midpoint P06 P19 P00)
    (h03 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h04 : between P12 P13 P14)
    : equal_length P03 P17 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0791
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0791

theorem v06_sealed_holdout_0792
    (P02 P03 P09 P12 P13 P14 P16 P19 P20 P22 P23 P24 P25 P27 P28 P31 : Point)
    (L04 : Line)
    (h00 : area_eq P24 P20 P22 P02 P12 P23)
    (h01 : area_eq P02 P12 P23 P03 P13 P25)
    (h02 : angle_bisector_line P14 P23 P16 P27 L04)
    (h03 : midpoint P16 P09 P02)
    (h04 : area_le P19 P22 P25 P28 P31 P02)
    : area_eq P24 P20 P22 P03 P13 P25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0792
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0792

theorem v06_sealed_holdout_0793
    (P03 P04 P05 P06 P09 P13 P14 P15 P16 P17 P18 P19 P23 P26 P27 P31 : Point)
    (L18 : Line)
    (C18 : Circle)
    (h00 : equal_length P05 P17 P16 P27)
    (h01 : equal_length P16 P27 P06 P15)
    (h02 : line_circle_intersection P03 L18 C18)
    (h03 : between P23 P18 P13)
    (h04 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    : equal_length P05 P17 P06 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0793
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0793

theorem v06_sealed_holdout_0794
    (P01 P02 P03 P04 P06 P08 P15 P17 P19 P21 P22 P25 P27 P28 : Point)
    (L14 L24 : Line)
    (C02 C30 : Circle)
    (h00 : angle_bisector_line P27 P02 P25 P03 L14)
    (h01 : circle_circle_intersection P19 C30 C02)
    (h02 : angle_bisector_line P21 P22 P17 P28 L24)
    (h03 : midpoint P01 P08 P15)
    (h04 : between P04 P21 P06)
    : angle_bisector P27 P02 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0794
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0794

theorem v06_sealed_holdout_0795
    (P02 P03 P04 P05 P10 P12 P21 P23 P24 P31 : Point)
    (L12 : Line)
    (C02 C18 : Circle)
    (h00 : angle_bisector_line P23 P03 P24 P04 L12)
    (h01 : midpoint P31 P10 P21)
    (h02 : midpoint P02 P23 P12)
    (h03 : between P05 P04 P03)
    (h04 : circle_circle_intersection P03 C02 C18)
    : angle_bisector P23 P03 P24 P04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0795
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0795

theorem v06_sealed_holdout_0796
    (P00 P04 P05 P07 P10 P12 P13 P14 P15 P16 P19 P23 P24 P26 P31 : Point)
    (C02 C22 : Circle)
    (h00 : directed_angle_eq_mod_pi P00 P10 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : midpoint P12 P13 P14)
    (h04 : midpoint P15 P26 P05)
    : directed_angle_eq_mod_pi P00 P10 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0796
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0796

theorem v06_sealed_holdout_0797
    (P02 P03 P07 P09 P10 P13 P16 P19 P21 P22 P23 P25 P28 P29 P30 P31 : Point)
    (h00 : directed_angle_eq_mod_2pi P21 P13 P10 P22 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P22 P30 P07 P16 P25 P02)
    (h02 : midpoint P16 P09 P02)
    (h03 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    (h04 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    : directed_angle_eq_mod_2pi P21 P13 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0797
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0797

theorem v06_sealed_holdout_0798
    (P02 P03 P04 P07 P08 P10 P13 P15 P16 P18 P19 P23 P24 P25 P26 P27 P30 P31 : Point)
    (L08 : Line)
    (C02 C06 : Circle)
    (h00 : directed_angle_eq_mod_pi P02 P10 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    (h03 : angle_bisector_line P25 P26 P16 P27 L08)
    (h04 : circle_circle_intersection P19 C06 C02)
    : directed_angle_eq_mod_pi P02 P10 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0798
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0798

theorem v06_sealed_holdout_0799
    (P01 P02 P04 P06 P07 P08 P10 P13 P15 P16 P18 P21 P22 P23 P24 P25 P27 P29 P30 : Point)
    (h00 : directed_angle_eq_mod_2pi P23 P13 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : area_le P30 P27 P24 P21 P18 P15)
    (h03 : area_le P01 P08 P15 P22 P29 P04)
    (h04 : midpoint P04 P21 P06)
    : directed_angle_eq_mod_2pi P23 P13 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0799
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0799

theorem v06_sealed_holdout_0800
    (P00 P01 P02 P03 P04 P05 P08 P11 P12 P16 P17 P19 P22 P23 P24 P26 : Point)
    (C02 C15 C30 : Circle)
    (h00 : circle_through_three_noncollinear_points P12 P24 P16 C15)
    (h01 : area_le P02 P23 P12 P01 P22 P11)
    (h02 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    (h03 : midpoint P08 P17 P26)
    (h04 : circle_circle_intersection P19 C30 C02)
    : triangle_pred P12 P24 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0800
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0800

theorem v06_sealed_holdout_0801
    (P00 P01 P05 P06 P07 P09 P12 P13 P14 P15 P16 P17 P18 P19 P23 P24 P27 P28 : Point)
    (L26 : Line)
    (C20 : Circle)
    (h00 : equilateral P01 P24 P06)
    (h01 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h02 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h03 : line_circle_intersection P19 L26 C20)
    (h04 : directed_angle_eq_mod_pi P18 P07 P28 P17 P06 P27)
    : triangle_pred P01 P24 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0801
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0801

theorem v06_sealed_holdout_0802
    (P02 P09 P13 P14 P16 P19 P20 P23 P24 P25 P27 P28 P29 : Point)
    (L10 L24 L28 : Line)
    (C16 C29 : Circle)
    (h00 : circle_through_three_noncollinear_points P14 P25 P16 C29)
    (h01 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    (h02 : angle_bisector_line P24 P23 P16 P27 L28)
    (h03 : angle_bisector_line P29 P27 P16 P28 L24)
    (h04 : line_circle_intersection P19 L10 C16)
    : triangle_pred P14 P25 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0802
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0802

theorem v06_sealed_holdout_0803
    (P03 P04 P06 P09 P13 P14 P18 P19 P23 P24 P26 P31 : Point)
    (L18 : Line)
    (C02 C06 C26 : Circle)
    (h00 : equilateral P03 P24 P06)
    (h01 : between P23 P18 P13)
    (h02 : area_le P26 P31 P04 P09 P14 P19)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : line_circle_intersection P03 L18 C26)
    : triangle_pred P03 P24 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0803
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0803

theorem v06_sealed_holdout_0804
    (P01 P02 P04 P06 P07 P08 P15 P18 P21 P22 P24 P27 P29 P30 : Point)
    (h00 : equilateral P04 P24 P06)
    (h01 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    (h02 : directed_angle_eq_mod_pi P01 P08 P15 P22 P29 P04)
    (h03 : midpoint P04 P21 P06)
    (h04 : between P07 P02 P29)
    : triangle_pred P04 P24 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0804
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0804

theorem v06_sealed_holdout_0805
    (P01 P02 P03 P05 P08 P11 P12 P14 P16 P17 P20 P22 P23 P27 P30 P31 : Point)
    (L04 L18 : Line)
    (C10 : Circle)
    (RF48 : Reflection)
    (h00 : area_le P02 P23 P12 P01 P22 P11)
    (h01 : angle_bisector_line P22 P20 P16 P27 L04)
    (h02 : line_circle_intersection P03 L18 C10)
    (h03 : midpoint P11 P30 P17)
    (h04 : area_le P14 P11 P08 P05 P02 P31)
    : reflection_image RF48 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0805
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0805

theorem v06_sealed_holdout_0806
    (P00 P03 P05 P06 P07 P09 P15 P16 P17 P18 P23 P26 P27 P28 P30 : Point)
    (L04 L18 : Line)
    (C02 : Circle)
    (HOM29 : Homothety)
    (h00 : midpoint P09 P00 P23)
    (h01 : line_circle_intersection P03 L18 C02)
    (h02 : midpoint P15 P26 P05)
    (h03 : area_le P18 P07 P28 P17 P06 P27)
    (h04 : angle_bisector_line P06 P30 P16 P27 L04)
    : homothety_image HOM29 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0806
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0806

theorem v06_sealed_holdout_0807
    (P02 P03 P16 P19 P22 P25 P28 P29 P30 P31 : Point)
    (L18 : Line)
    (C02 C22 C26 : Circle)
    (INV14 : Inversion)
    (h00 : line_circle_intersection P03 L18 C26)
    (h01 : area_le P19 P22 P25 P28 P31 P02)
    (h02 : midpoint P22 P03 P16)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : midpoint P28 P29 P30)
    : inversion_image INV14 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0807
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0807

theorem v06_sealed_holdout_0808
    (P03 P04 P09 P12 P14 P19 P26 P27 P29 P31 : Point)
    (L26 : Line)
    (C02 C04 C18 C30 : Circle)
    (SP03 : SpiralSimilarity)
    (h00 : line_circle_intersection P19 L26 C04)
    (h01 : area_le P26 P31 P04 P09 P14 P19)
    (h02 : between P29 P12 P27)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : circle_circle_intersection P19 C30 C02)
    : spiral_similarity_center SP03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0808
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0808

theorem v06_sealed_holdout_0809
    (P03 P08 P19 P24 P28 P29 P31 : Point)
    (L02 : Line)
    (C02 C14 C22 : Circle)
    (h00 : P29 = P08)
    (h01 : P24 = P19)
    (h02 : P28 = P31)
    (h03 : circle_circle_intersection P19 C14 C02)
    (h04 : line_circle_intersection P03 L02 C22)
    : rotation_preserves_collinear P29 P24 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0809
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0809

theorem v06_sealed_holdout_0810
    (P02 P05 P06 P08 P11 P14 P16 P17 P20 P24 P27 P28 P30 P31 : Point)
    (L00 : Line)
    (C07 : Circle)
    (h00 : circle_with_center_through_point P06 P11 C07)
    (h01 : angle_bisector_line P27 P20 P16 P28 L00)
    (h02 : midpoint P11 P30 P17)
    (h03 : area_le P14 P11 P08 P05 P02 P31)
    (h04 : midpoint P17 P24 P31)
    : on_circle P11 C07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0810
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0810

theorem v06_sealed_holdout_0811
    (P01 P04 P05 P06 P07 P10 P16 P17 P18 P19 P20 P21 P24 P27 P28 P29 : Point)
    (L21 L28 : Line)
    (C29 : Circle)
    (h00 : line_circle_intersection P04 L21 C29)
    (h01 : directed_angle_eq_mod_pi P18 P07 P28 P17 P06 P27)
    (h02 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    (h03 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    (h04 : angle_bisector_line P16 P29 P17 P28 L28)
    : on_circle P04 C29 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0811
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0811

theorem v06_sealed_holdout_0812
    (P01 P02 P03 P10 P11 P12 P19 P22 P23 : Point)
    (L26 : Line)
    (C02 C12 C18 C19 C20 C22 : Circle)
    (h00 : chord P01 P10 C12)
    (h01 : circle_circle_intersection P19 C22 C02)
    (h02 : circle_circle_intersection P03 C18 C19)
    (h03 : line_circle_intersection P19 L26 C20)
    (h04 : directed_angle_eq_mod_pi P02 P23 P12 P01 P22 P11)
    : on_circle P01 C12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0812
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0812

theorem v06_sealed_holdout_0813
    (P00 P03 P05 P06 P07 P09 P13 P14 P19 P23 P26 P28 : Point)
    (L13 : Line)
    (C02 C18 C19 C20 C30 : Circle)
    (h00 : line_circle_intersection P23 L13 C20)
    (h01 : circle_circle_intersection P19 C30 C02)
    (h02 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    (h03 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h04 : circle_circle_intersection P03 C18 C19)
    : on_line P23 L13 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0813
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0813

theorem v06_sealed_holdout_0814
    (P02 P09 P11 P12 P13 P14 P16 P18 P19 P20 P23 P24 P26 P27 P28 : Point)
    (L08 L25 : Line)
    (C02 C30 : Circle)
    (h00 : altitude P12 P27 P14 P23 L25)
    (h01 : angle_bisector_line P09 P19 P18 P28 L08)
    (h02 : directed_angle_eq_mod_pi P13 P28 P11 P26 P09 P24)
    (h03 : area_le P16 P09 P02 P27 P20 P13)
    (h04 : circle_circle_intersection P19 C30 C02)
    : on_line P14 L25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0814
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0814

theorem v06_sealed_holdout_0815
    (P02 P03 P05 P08 P11 P13 P14 P17 P18 P23 P24 P27 P30 P31 : Point)
    (L19 : Line)
    (C18 C19 : Circle)
    (h00 : altitude P08 P27 P13 P23 L19)
    (h01 : area_le P14 P11 P08 P05 P02 P31)
    (h02 : between P17 P24 P31)
    (h03 : circle_circle_intersection P03 C18 C19)
    (h04 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    : on_line P13 L19 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0815
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0815

theorem v06_sealed_holdout_0816
    (P01 P04 P05 P06 P07 P10 P12 P14 P16 P17 P18 P19 P20 P21 P23 P24 P27 P28 : Point)
    (L13 : Line)
    (h00 : altitude P04 P28 P12 P23 L13)
    (h01 : area_le P18 P07 P28 P17 P06 P27)
    (h02 : area_le P21 P20 P19 P18 P17 P16)
    (h03 : area_le P24 P01 P10 P19 P28 P05)
    (h04 : midpoint P27 P14 P01)
    : on_line P12 L13 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0816
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0816

theorem v06_sealed_holdout_0817
    (P00 P01 P02 P03 P04 P05 P19 P22 P28 P29 P30 : Point)
    (L24 : Line)
    (C02 C10 C12 C14 C18 : Circle)
    (h00 : line_circle_intersection P22 L24 C12)
    (h01 : midpoint P28 P29 P30)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    : on_line P22 L24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0817
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0817

theorem v06_sealed_holdout_0818
    (P00 P01 P03 P06 P09 P17 P19 P20 P23 P28 P29 : Point)
    (L16 : Line)
    (C02 C22 : Circle)
    (h00 : equilateral P03 P20 P01)
    (h01 : between P03 P06 P09)
    (h02 : between P06 P19 P00)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : angle_bisector_line P23 P29 P17 P28 L16)
    : equal_length P03 P20 P20 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0818
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0818

theorem v06_sealed_holdout_0819
    (P00 P02 P07 P09 P10 P11 P13 P15 P16 P20 P21 P28 P29 P31 : Point)
    (h00 : equilateral P31 P21 P00)
    (h01 : between P07 P02 P29)
    (h02 : midpoint P10 P15 P20)
    (h03 : midpoint P13 P28 P11)
    (h04 : midpoint P16 P09 P02)
    : equal_length P31 P21 P21 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0819
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0819

theorem v06_sealed_holdout_0820
    (P04 P05 P07 P09 P16 P19 P20 P21 P22 P23 P24 P27 P30 : Point)
    (L10 L24 : Line)
    (C00 C02 C14 : Circle)
    (h00 : length_sum P04 P07 P30 P09 P16 P23)
    (h01 : angle_bisector_line P05 P21 P16 P27 L24)
    (h02 : line_circle_intersection P19 L10 C00)
    (h03 : directed_angle_eq_mod_pi P20 P05 P22 P07 P24 P09)
    (h04 : circle_circle_intersection P19 C14 C02)
    : length_sum P30 P09 P04 P07 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0820
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0820

theorem v06_sealed_holdout_0821
    (P01 P05 P07 P10 P14 P15 P16 P18 P19 P20 P24 P26 P27 P28 P30 : Point)
    (h00 : equal_length P01 P18 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : area_le P24 P01 P10 P19 P28 P05)
    (h03 : area_le P27 P14 P01 P20 P07 P26)
    (h04 : between P30 P27 P24)
    : equal_length P01 P18 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0821
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0821

theorem v06_sealed_holdout_0822
    (P02 P03 P04 P05 P12 P13 P19 P21 P22 P23 P24 P25 : Point)
    (L26 : Line)
    (C20 : Circle)
    (h00 : area_eq P22 P21 P23 P02 P12 P24)
    (h01 : area_eq P02 P12 P24 P03 P13 P25)
    (h02 : line_circle_intersection P19 L26 C20)
    (h03 : midpoint P02 P23 P12)
    (h04 : between P05 P04 P03)
    : area_eq P22 P21 P23 P03 P13 P25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0822
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0822

theorem v06_sealed_holdout_0823
    (P03 P05 P13 P15 P16 P18 P24 P27 P28 : Point)
    (L20 L24 : Line)
    (C18 C19 : Circle)
    (h00 : equal_length P03 P18 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : angle_bisector_line P13 P24 P16 P27 L24)
    (h03 : angle_bisector_line P18 P27 P16 P28 L20)
    (h04 : circle_circle_intersection P03 C18 C19)
    : equal_length P03 P18 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0823
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0823

theorem v06_sealed_holdout_0824
    (P02 P03 P04 P09 P16 P19 P22 P25 P26 : Point)
    (L10 L16 : Line)
    (C08 : Circle)
    (h00 : angle_bisector_line P25 P03 P26 P04 L16)
    (h01 : line_circle_intersection P19 L10 C08)
    (h02 : midpoint P16 P09 P02)
    (h03 : between P19 P22 P25)
    (h04 : between P22 P03 P16)
    : angle_bisector P25 P03 P26 P04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0824
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0824

theorem v06_sealed_holdout_0825
    (P03 P04 P10 P16 P20 P21 P24 P27 P28 : Point)
    (L12 L14 L18 L20 : Line)
    (C10 C18 : Circle)
    (h00 : angle_bisector_line P21 P04 P24 P03 L14)
    (h01 : angle_bisector_line P10 P21 P16 P27 L20)
    (h02 : line_circle_intersection P03 L18 C18)
    (h03 : angle_bisector_line P20 P27 P16 P28 L12)
    (h04 : circle_circle_intersection P03 C10 C18)
    : angle_bisector P21 P04 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0825
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0825

theorem v06_sealed_holdout_0826
    (P01 P04 P07 P08 P11 P15 P16 P18 P19 P21 P23 P24 P27 P30 P31 : Point)
    (C02 C30 : Circle)
    (h00 : directed_angle_eq_mod_pi P30 P11 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    (h04 : between P01 P08 P15)
    : directed_angle_eq_mod_pi P30 P11 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0826
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0826

theorem v06_sealed_holdout_0827
    (P02 P03 P04 P05 P07 P10 P12 P14 P16 P19 P21 P23 P25 P30 : Point)
    (C02 C18 : Circle)
    (h00 : directed_angle_eq_mod_2pi P19 P14 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : between P02 P23 P12)
    (h03 : midpoint P05 P04 P03)
    (h04 : circle_circle_intersection P03 C02 C18)
    : directed_angle_eq_mod_2pi P19 P14 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0827
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0827

theorem v06_sealed_holdout_0828
    (P00 P04 P07 P09 P11 P12 P13 P14 P15 P16 P19 P23 P24 P31 : Point)
    (C02 C14 : Circle)
    (h00 : directed_angle_eq_mod_pi P00 P11 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : between P09 P00 P23)
    (h03 : between P12 P13 P14)
    (h04 : circle_circle_intersection P19 C14 C02)
    : directed_angle_eq_mod_pi P00 P11 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0828
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0828

theorem v06_sealed_holdout_0829
    (P02 P03 P07 P10 P14 P16 P19 P21 P22 P24 P25 P27 P30 : Point)
    (L00 L02 : Line)
    (C02 C30 : Circle)
    (h00 : directed_angle_eq_mod_2pi P21 P14 P10 P22 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P22 P30 P07 P16 P25 P02)
    (h02 : angle_bisector_line P19 P24 P16 P27 L00)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : line_circle_intersection P03 L02 C30)
    : directed_angle_eq_mod_2pi P21 P14 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0829
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0829

theorem v06_sealed_holdout_0830
    (P03 P04 P10 P12 P13 P16 P18 P23 P25 P26 P27 P29 P31 : Point)
    (C01 C18 C19 : Circle)
    (h00 : circle_through_three_noncollinear_points P10 P25 P16 C01)
    (h01 : circle_circle_intersection P03 C18 C19)
    (h02 : midpoint P23 P18 P13)
    (h03 : midpoint P26 P31 P04)
    (h04 : midpoint P29 P12 P27)
    : triangle_pred P10 P25 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0830
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0830

theorem v06_sealed_holdout_0831
    (P01 P04 P06 P08 P15 P19 P21 P22 P24 P25 P27 P29 P30 P31 : Point)
    (L26 : Line)
    (C28 : Circle)
    (h00 : equilateral P31 P25 P06)
    (h01 : line_circle_intersection P19 L26 C28)
    (h02 : between P30 P27 P24)
    (h03 : area_le P01 P08 P15 P22 P29 P04)
    (h04 : between P04 P21 P06)
    : triangle_pred P31 P25 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0831
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0831

theorem v06_sealed_holdout_0832
    (P03 P04 P10 P11 P12 P16 P17 P19 P23 P25 P30 : Point)
    (L02 L10 : Line)
    (C02 C06 C15 C18 C24 : Circle)
    (h00 : circle_through_three_noncollinear_points P12 P25 P16 C15)
    (h01 : line_circle_intersection P03 L02 C06)
    (h02 : line_circle_intersection P19 L10 C24)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : area_le P11 P30 P17 P04 P23 P10)
    : triangle_pred P12 P25 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0832
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0832

theorem v06_sealed_holdout_0833
    (P01 P03 P06 P16 P19 P23 P24 P25 P27 P28 P29 : Point)
    (L02 L12 L16 : Line)
    (C02 C06 C22 : Circle)
    (h00 : equilateral P01 P25 P06)
    (h01 : circle_circle_intersection P19 C22 C02)
    (h02 : angle_bisector_line P23 P24 P16 P27 L16)
    (h03 : angle_bisector_line P28 P27 P16 P29 L12)
    (h04 : line_circle_intersection P03 L02 C06)
    : triangle_pred P01 P25 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0833
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0833

theorem v06_sealed_holdout_0834
    (P02 P03 P06 P07 P09 P16 P19 P25 : Point)
    (L02 L26 : Line)
    (C12 C30 : Circle)
    (h00 : equilateral P02 P25 P06)
    (h01 : between P16 P09 P02)
    (h02 : line_circle_intersection P19 L26 C12)
    (h03 : line_circle_intersection P03 L02 C30)
    (h04 : midpoint P25 P16 P07)
    : triangle_pred P02 P25 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0834
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0834

theorem v06_sealed_holdout_0835
    (P03 P15 P16 P18 P19 P27 P31 : Point)
    (L00 L16 L26 : Line)
    (C02 C04 C06 C10 C18 : Circle)
    (RF02 : Reflection)
    (h00 : angle_bisector_line P15 P18 P16 P27 L16)
    (h01 : line_circle_intersection P19 L26 C04)
    (h02 : circle_circle_intersection P03 C10 C18)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : angle_bisector_line P03 P31 P16 P27 L00)
    : reflection_image RF02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0835
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0835

theorem v06_sealed_holdout_0836
    (P02 P04 P06 P07 P08 P15 P18 P19 P21 P23 P24 P25 P27 P29 P30 : Point)
    (L26 : Line)
    (C02 C22 C28 : Circle)
    (HOM43 : Homothety)
    (h00 : line_circle_intersection P19 L26 C28)
    (h01 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    (h04 : midpoint P07 P02 P29)
    : homothety_image HOM43 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0836
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0836

theorem v06_sealed_holdout_0837
    (P02 P03 P04 P05 P08 P10 P11 P12 P17 P23 P26 P30 : Point)
    (C18 C26 : Circle)
    (INV24 : Inversion)
    (h00 : midpoint P02 P23 P12)
    (h01 : between P05 P04 P03)
    (h02 : midpoint P08 P17 P26)
    (h03 : area_le P11 P30 P17 P04 P23 P10)
    (h04 : circle_circle_intersection P03 C26 C18)
    : inversion_image INV24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0837
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0837

theorem v06_sealed_holdout_0838
    (P00 P05 P06 P07 P09 P12 P13 P14 P15 P16 P17 P18 P19 P23 P26 P27 P28 : Point)
    (L10 : Line)
    (C24 : Circle)
    (SP09 : SpiralSimilarity)
    (h00 : area_le P09 P00 P23 P14 P05 P28)
    (h01 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h02 : area_le P15 P26 P05 P16 P27 P06)
    (h03 : directed_angle_eq_mod_pi P18 P07 P28 P17 P06 P27)
    (h04 : line_circle_intersection P19 L10 C24)
    : spiral_similarity_center SP09 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0838
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0838

theorem v06_sealed_holdout_0839
    (P00 P01 P08 P19 P25 P27 P28 P29 P30 P31 : Point)
    (L10 : Line)
    (C16 : Circle)
    (h00 : P27 = P08)
    (h01 : P25 = P19)
    (h02 : P28 = P31)
    (h03 : line_circle_intersection P19 L10 C16)
    (h04 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    : rotation_preserves_collinear P27 P25 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0839
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0839

theorem v06_sealed_holdout_0840
    (P03 P04 P08 P12 P16 P19 P26 P27 P31 : Point)
    (L10 L28 : Line)
    (C02 C08 C11 C18 : Circle)
    (h00 : circle_with_center_through_point P04 P12 C11)
    (h01 : midpoint P26 P31 P04)
    (h02 : line_circle_intersection P19 L10 C08)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : angle_bisector_line P08 P31 P16 P27 L28)
    : on_circle P12 C11 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0840
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0840

theorem v06_sealed_holdout_0841
    (P02 P03 P04 P06 P08 P09 P11 P13 P17 P21 P23 P24 P25 P26 P28 : Point)
    (L02 L12 L21 : Line)
    (C11 C22 : Circle)
    (h00 : line_circle_intersection P02 L21 C11)
    (h01 : area_le P04 P21 P06 P23 P08 P25)
    (h02 : angle_bisector_line P04 P24 P17 P28 L12)
    (h03 : line_circle_intersection P03 L02 C22)
    (h04 : area_le P13 P28 P11 P26 P09 P24)
    : on_circle P02 C11 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0841
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0841

theorem v06_sealed_holdout_0842
    (P05 P07 P08 P09 P11 P14 P17 P19 P20 P22 P24 P30 P31 : Point)
    (L10 : Line)
    (C00 C20 : Circle)
    (h00 : chord P31 P11 C20)
    (h01 : midpoint P11 P30 P17)
    (h02 : between P14 P11 P08)
    (h03 : line_circle_intersection P19 L10 C00)
    (h04 : area_le P20 P05 P22 P07 P24 P09)
    : on_circle P31 C20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0842
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0842

theorem v06_sealed_holdout_0843
    (P01 P05 P10 P16 P17 P18 P19 P20 P21 P24 P28 P29 : Point)
    (L15 L24 L26 : Line)
    (C04 C28 : Circle)
    (h00 : line_circle_intersection P21 L15 C04)
    (h01 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    (h02 : area_le P24 P01 P10 P19 P28 P05)
    (h03 : line_circle_intersection P19 L26 C28)
    (h04 : angle_bisector_line P21 P29 P18 P28 L24)
    : on_line P21 L15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0843
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0843

theorem v06_sealed_holdout_0844
    (P00 P02 P03 P10 P11 P17 P21 P22 P28 P31 : Point)
    (L02 L13 L20 : Line)
    (C04 C06 C18 C19 : Circle)
    (h00 : line_circle_intersection P17 L13 C04)
    (h01 : angle_bisector_line P02 P21 P17 P28 L20)
    (h02 : circle_circle_intersection P03 C18 C19)
    (h03 : area_le P31 P10 P21 P00 P11 P22)
    (h04 : line_circle_intersection P03 L02 C06)
    : on_line P17 L13 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0844
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0844

theorem v06_sealed_holdout_0845
    (P00 P03 P06 P07 P09 P13 P17 P19 P21 P23 P26 P28 : Point)
    (L00 L25 : Line)
    (C02 C30 : Circle)
    (h00 : altitude P06 P28 P13 P23 L25)
    (h01 : angle_bisector_line P03 P21 P17 P28 L00)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    (h04 : midpoint P09 P00 P23)
    : on_line P13 L25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0845
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0845

theorem v06_sealed_holdout_0846
    (P02 P03 P07 P12 P19 P23 P29 : Point)
    (L10 L19 : Line)
    (C08 C10 C18 C19 : Circle)
    (h00 : altitude P02 P29 P12 P23 L19)
    (h01 : circle_circle_intersection P03 C18 C19)
    (h02 : midpoint P07 P02 P29)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : line_circle_intersection P19 L10 C08)
    : on_line P12 L19 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0846
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0846

theorem v06_sealed_holdout_0847
    (P03 P17 P19 P20 P24 P31 : Point)
    (L02 L18 L26 : Line)
    (C04 C14 C18 C28 : Circle)
    (h00 : line_circle_intersection P20 L26 C28)
    (h01 : line_circle_intersection P03 L02 C14)
    (h02 : between P17 P24 P31)
    (h03 : line_circle_intersection P03 L18 C18)
    (h04 : line_circle_intersection P19 L26 C04)
    : on_line P20 L26 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0847
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0847

theorem v06_sealed_holdout_0848
    (P01 P02 P03 P07 P14 P15 P18 P19 P20 P21 P24 P26 P27 P30 : Point)
    (C02 C06 C18 : Circle)
    (h00 : equilateral P01 P21 P02)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    (h04 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    : equal_length P01 P21 P21 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0848
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0848

theorem v06_sealed_holdout_0849
    (P00 P01 P02 P10 P11 P12 P16 P21 P22 P23 P27 P28 P29 P30 P31 : Point)
    (L20 : Line)
    (h00 : equilateral P29 P22 P00)
    (h01 : angle_bisector_line P02 P22 P16 P27 L20)
    (h02 : between P28 P29 P30)
    (h03 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    (h04 : directed_angle_eq_mod_pi P02 P23 P12 P01 P22 P11)
    : equal_length P29 P22 P22 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0849
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0849

theorem v06_sealed_holdout_0850
    (P00 P02 P03 P04 P06 P08 P09 P11 P13 P16 P18 P23 P25 P27 P28 P29 P30 P31 : Point)
    (L20 L24 : Line)
    (h00 : length_sum P02 P08 P30 P09 P16 P23)
    (h01 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    (h02 : midpoint P03 P06 P09)
    (h03 : angle_bisector_line P13 P28 P16 P27 L24)
    (h04 : angle_bisector_line P18 P31 P16 P27 L20)
    : length_sum P30 P09 P02 P08 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0850
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0850

theorem v06_sealed_holdout_0851
    (P02 P03 P05 P09 P11 P13 P15 P16 P19 P27 P28 P31 : Point)
    (L02 : Line)
    (C22 : Circle)
    (h00 : equal_length P31 P19 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : line_circle_intersection P03 L02 C22)
    (h03 : between P13 P28 P11)
    (h04 : midpoint P16 P09 P02)
    : equal_length P31 P19 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0851
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0851

theorem v06_sealed_holdout_0852
    (P02 P03 P05 P07 P09 P10 P12 P13 P16 P18 P20 P22 P23 P24 P25 P27 : Point)
    (L20 : Line)
    (h00 : area_eq P20 P22 P23 P02 P12 P24)
    (h01 : area_eq P02 P12 P24 P03 P13 P25)
    (h02 : angle_bisector_line P10 P25 P16 P27 L20)
    (h03 : directed_angle_eq_mod_pi P20 P05 P22 P07 P24 P09)
    (h04 : between P23 P18 P13)
    : area_eq P20 P22 P23 P03 P13 P25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0852
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0852

theorem v06_sealed_holdout_0853
    (P01 P05 P10 P15 P16 P19 P24 P27 P30 : Point)
    (C02 C30 : Circle)
    (h00 : equal_length P01 P19 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : midpoint P24 P01 P10)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : between P30 P27 P24)
    : equal_length P01 P19 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0853
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0853

theorem v06_sealed_holdout_0854
    (P03 P04 P08 P12 P17 P19 P21 P23 P25 P26 : Point)
    (L18 : Line)
    (C02 C06 C10 C14 C18 : Circle)
    (h00 : angle_bisector_line P23 P04 P25 P03 L18)
    (h01 : circle_circle_intersection P19 C14 C02)
    (h02 : circle_circle_intersection P03 C10 C18)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : area_le P08 P17 P26 P03 P12 P21)
    : angle_bisector P23 P04 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0854
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0854

theorem v06_sealed_holdout_0855
    (P00 P03 P05 P06 P09 P14 P19 P23 P24 P28 : Point)
    (L16 L18 : Line)
    (C02 C30 : Circle)
    (h00 : angle_bisector_line P19 P05 P24 P03 L16)
    (h01 : circle_circle_intersection P19 C30 C02)
    (h02 : between P06 P19 P00)
    (h03 : area_le P09 P00 P23 P14 P05 P28)
    (h04 : line_circle_intersection P03 L18 C02)
    : angle_bisector P19 P05 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0855
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0855

theorem v06_sealed_holdout_0856
    (P02 P04 P07 P09 P11 P12 P13 P15 P16 P19 P20 P22 P23 P24 P25 P26 P27 P28 P31 : Point)
    (h00 : directed_angle_eq_mod_pi P28 P12 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : area_le P13 P28 P11 P26 P09 P24)
    (h03 : area_le P16 P09 P02 P27 P20 P13)
    (h04 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    : directed_angle_eq_mod_pi P28 P12 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0856
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0856

theorem v06_sealed_holdout_0857
    (P02 P04 P05 P07 P10 P13 P15 P16 P17 P18 P20 P21 P22 P23 P25 P26 P30 P31 : Point)
    (h00 : directed_angle_eq_mod_2pi P17 P15 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : between P20 P05 P22)
    (h03 : between P23 P18 P13)
    (h04 : between P26 P31 P04)
    : directed_angle_eq_mod_2pi P17 P15 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0857
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0857

theorem v06_sealed_holdout_0858
    (P01 P04 P07 P12 P14 P15 P16 P19 P20 P23 P24 P26 P27 P30 P31 : Point)
    (L10 : Line)
    (C00 : Circle)
    (h00 : directed_angle_eq_mod_pi P30 P12 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : area_le P27 P14 P01 P20 P07 P26)
    (h03 : between P30 P27 P24)
    (h04 : line_circle_intersection P19 L10 C00)
    : directed_angle_eq_mod_pi P30 P12 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0858
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0858

theorem v06_sealed_holdout_0859
    (P02 P03 P04 P05 P07 P08 P10 P12 P15 P16 P17 P19 P21 P23 P25 P26 P30 : Point)
    (h00 : directed_angle_eq_mod_2pi P19 P15 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : between P02 P23 P12)
    (h03 : between P05 P04 P03)
    (h04 : directed_angle_eq_mod_pi P08 P17 P26 P03 P12 P21)
    : directed_angle_eq_mod_2pi P19 P15 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0859
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0859

theorem v06_sealed_holdout_0860
    (P03 P05 P08 P13 P15 P16 P19 P22 P26 P27 : Point)
    (L10 L18 L24 : Line)
    (C02 C16 C19 : Circle)
    (h00 : circle_through_three_noncollinear_points P08 P26 P16 C19)
    (h01 : angle_bisector_line P13 P22 P16 P27 L24)
    (h02 : line_circle_intersection P19 L10 C16)
    (h03 : line_circle_intersection P03 L18 C02)
    (h04 : midpoint P15 P26 P05)
    : triangle_pred P08 P26 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0860
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0860

theorem v06_sealed_holdout_0861
    (P03 P06 P09 P11 P13 P16 P24 P26 P27 P28 P29 : Point)
    (L18 L28 : Line)
    (C18 C26 : Circle)
    (h00 : equilateral P29 P26 P06)
    (h01 : directed_angle_eq_mod_pi P13 P28 P11 P26 P09 P24)
    (h02 : line_circle_intersection P03 L18 C26)
    (h03 : angle_bisector_line P24 P28 P16 P27 L28)
    (h04 : circle_circle_intersection P03 C26 C18)
    : triangle_pred P29 P26 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0861
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0861

theorem v06_sealed_holdout_0862
    (P03 P10 P13 P16 P18 P19 P23 P26 : Point)
    (L10 : Line)
    (C01 C08 C10 C18 C19 : Circle)
    (h00 : circle_through_three_noncollinear_points P10 P26 P16 C01)
    (h01 : circle_circle_intersection P03 C18 C19)
    (h02 : midpoint P23 P18 P13)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : line_circle_intersection P19 L10 C08)
    : triangle_pred P10 P26 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0862
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0862

theorem v06_sealed_holdout_0863
    (P01 P04 P06 P07 P08 P14 P15 P20 P21 P22 P24 P26 P27 P29 P30 P31 : Point)
    (h00 : equilateral P31 P26 P06)
    (h01 : area_le P27 P14 P01 P20 P07 P26)
    (h02 : midpoint P30 P27 P24)
    (h03 : directed_angle_eq_mod_pi P01 P08 P15 P22 P29 P04)
    (h04 : between P04 P21 P06)
    : triangle_pred P31 P26 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0863
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0863

theorem v06_sealed_holdout_0864
    (P00 P01 P02 P03 P04 P05 P06 P08 P10 P11 P12 P17 P21 P22 P23 P26 P30 : Point)
    (h00 : equilateral P00 P26 P06)
    (h01 : area_le P02 P23 P12 P01 P22 P11)
    (h02 : between P05 P04 P03)
    (h03 : directed_angle_eq_mod_pi P08 P17 P26 P03 P12 P21)
    (h04 : area_le P11 P30 P17 P04 P23 P10)
    : triangle_pred P00 P26 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0864
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0864

theorem v06_sealed_holdout_0865
    (P00 P03 P05 P06 P07 P09 P14 P15 P18 P19 P23 P26 P28 : Point)
    (L18 : Line)
    (C02 : Circle)
    (RF20 : Reflection)
    (h00 : between P06 P19 P00)
    (h01 : area_le P09 P00 P23 P14 P05 P28)
    (h02 : line_circle_intersection P03 L18 C02)
    (h03 : midpoint P15 P26 P05)
    (h04 : midpoint P18 P07 P28)
    : reflection_image RF20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0865
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0865

theorem v06_sealed_holdout_0866
    (P03 P07 P11 P12 P13 P16 P19 P21 P25 P28 P30 : Point)
    (L02 : Line)
    (C02 C18 C30 : Circle)
    (HOM57 : Homothety)
    (h00 : between P13 P28 P11)
    (h01 : circle_circle_intersection P03 C02 C18)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : line_circle_intersection P03 L02 C30)
    (h04 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    : homothety_image HOM57 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0866
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0866

theorem v06_sealed_holdout_0867
    (P00 P04 P05 P16 P18 P19 P20 P22 P25 P26 P27 P31 : Point)
    (L12 : Line)
    (C02 C06 : Circle)
    (INV34 : Inversion)
    (h00 : between P20 P05 P22)
    (h01 : angle_bisector_line P20 P22 P16 P27 L12)
    (h02 : midpoint P26 P31 P04)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : midpoint P00 P25 P18)
    : inversion_image INV34 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0867
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0867

theorem v06_sealed_holdout_0868
    (P02 P03 P04 P06 P07 P08 P16 P17 P19 P21 P23 P25 P26 P27 P29 : Point)
    (L02 L20 L28 : Line)
    (C14 : Circle)
    (SP15 : SpiralSimilarity)
    (h00 : angle_bisector_line P16 P19 P17 P27 L28)
    (h01 : line_circle_intersection P03 L02 C14)
    (h02 : angle_bisector_line P26 P25 P16 P27 L20)
    (h03 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    (h04 : between P07 P02 P29)
    : spiral_similarity_center SP15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0868
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0868

theorem v06_sealed_holdout_0869
    (P08 P11 P14 P19 P25 P26 P28 P31 : Point)
    (L26 : Line)
    (C28 : Circle)
    (h00 : P25 = P08)
    (h01 : P26 = P19)
    (h02 : P28 = P31)
    (h03 : line_circle_intersection P19 L26 C28)
    (h04 : midpoint P14 P11 P08)
    : rotation_preserves_collinear P25 P26 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0869
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0869

theorem v06_sealed_holdout_0870
    (P02 P05 P06 P07 P12 P13 P14 P15 P16 P17 P18 P19 P20 P21 P26 P27 P28 : Point)
    (C15 : Circle)
    (h00 : circle_with_center_through_point P02 P13 C15)
    (h01 : area_le P12 P13 P14 P15 P16 P17)
    (h02 : area_le P15 P26 P05 P16 P27 P06)
    (h03 : directed_angle_eq_mod_pi P18 P07 P28 P17 P06 P27)
    (h04 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    : on_circle P13 C15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0870
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0870

theorem v06_sealed_holdout_0871
    (P00 P01 P03 P12 P17 P19 P28 P29 P30 P31 : Point)
    (L10 L12 L21 : Line)
    (C16 C18 C25 C26 : Circle)
    (h00 : line_circle_intersection P00 L21 C25)
    (h01 : circle_circle_intersection P03 C26 C18)
    (h02 : line_circle_intersection P19 L10 C16)
    (h03 : area_le P28 P29 P30 P31 P00 P01)
    (h04 : angle_bisector_line P12 P31 P17 P28 L12)
    : on_circle P00 C25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0871
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0871

theorem v06_sealed_holdout_0872
    (P00 P03 P04 P06 P09 P11 P12 P13 P15 P17 P18 P25 P27 P28 P29 P31 : Point)
    (L24 : Line)
    (C28 : Circle)
    (h00 : chord P29 P12 C28)
    (h01 : between P29 P12 P27)
    (h02 : area_le P00 P25 P18 P11 P04 P29)
    (h03 : directed_angle_eq_mod_pi P03 P06 P09 P12 P15 P18)
    (h04 : angle_bisector_line P13 P31 P17 P28 L24)
    : on_circle P29 C28 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0872
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0872

theorem v06_sealed_holdout_0873
    (P03 P09 P11 P13 P19 P24 P26 P28 : Point)
    (L17 : Line)
    (C02 C10 C14 C18 C20 : Circle)
    (h00 : line_circle_intersection P19 L17 C20)
    (h01 : circle_circle_intersection P19 C14 C02)
    (h02 : circle_circle_intersection P03 C10 C18)
    (h03 : area_le P13 P28 P11 P26 P09 P24)
    (h04 : circle_circle_intersection P03 C02 C18)
    : on_line P19 L17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0873
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0873

theorem v06_sealed_holdout_0874
    (P05 P11 P15 P17 P19 P20 P22 P25 P28 P30 : Point)
    (L10 L15 L24 : Line)
    (C00 C20 : Circle)
    (h00 : line_circle_intersection P15 L15 C20)
    (h01 : between P11 P30 P17)
    (h02 : angle_bisector_line P05 P25 P17 P28 L24)
    (h03 : line_circle_intersection P19 L10 C00)
    (h04 : midpoint P20 P05 P22)
    : on_line P15 L15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0874
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0874

theorem v06_sealed_holdout_0875
    (P01 P04 P05 P10 P13 P14 P17 P19 P22 P23 P24 P27 P28 P29 : Point)
    (L08 L10 L31 : Line)
    (C24 : Circle)
    (h00 : altitude P04 P29 P13 P23 L31)
    (h01 : angle_bisector_line P01 P22 P17 P28 L08)
    (h02 : line_circle_intersection P19 L10 C24)
    (h03 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    (h04 : between P27 P14 P01)
    : on_line P13 L31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0875
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0875

theorem v06_sealed_holdout_0876
    (P01 P07 P10 P12 P16 P17 P18 P19 P21 P25 P28 P29 P30 P31 : Point)
    (L04 L08 L16 : Line)
    (h00 : angle_bisector_line P25 P01 P19 P29 L04)
    (h01 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h02 : angle_bisector_line P07 P25 P17 P28 L16)
    (h03 : midpoint P31 P10 P21)
    (h04 : angle_bisector_line P17 P31 P18 P28 L08)
    : on_line P25 L04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0876
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0876

theorem v06_sealed_holdout_0877
    (P00 P03 P04 P06 P09 P11 P12 P15 P18 P19 P25 P29 : Point)
    (L10 L28 : Line)
    (C12 C16 : Circle)
    (h00 : line_circle_intersection P18 L28 C12)
    (h01 : area_le P00 P25 P18 P11 P04 P29)
    (h02 : directed_angle_eq_mod_pi P03 P06 P09 P12 P15 P18)
    (h03 : midpoint P06 P19 P00)
    (h04 : line_circle_intersection P19 L10 C16)
    : on_line P18 L28 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0877
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0877

theorem v06_sealed_holdout_0878
    (P01 P02 P03 P07 P11 P13 P17 P19 P22 P28 P29 P31 : Point)
    (L00 : Line)
    (C10 C18 : Circle)
    (h00 : equilateral P31 P22 P01)
    (h01 : between P07 P02 P29)
    (h02 : circle_circle_intersection P03 C10 C18)
    (h03 : midpoint P13 P28 P11)
    (h04 : angle_bisector_line P19 P31 P17 P28 L00)
    : equal_length P31 P22 P22 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0878
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0878

theorem v06_sealed_holdout_0879
    (P00 P03 P06 P13 P15 P16 P17 P19 P20 P23 P24 P27 P31 : Point)
    (L16 : Line)
    (C02 C18 C26 C30 : Circle)
    (h00 : equilateral P27 P23 P00)
    (h01 : circle_circle_intersection P19 C30 C02)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : area_le P17 P24 P31 P06 P13 P20)
    (h04 : angle_bisector_line P15 P00 P16 P27 L16)
    : equal_length P27 P23 P23 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0879
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0879

theorem v06_sealed_holdout_0880
    (P00 P01 P05 P06 P07 P09 P10 P14 P16 P17 P18 P19 P20 P21 P23 P24 P26 P27 P28 P30 : Point)
    (h00 : length_sum P00 P09 P30 P10 P16 P23)
    (h01 : area_le P18 P07 P28 P17 P06 P27)
    (h02 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    (h03 : area_le P24 P01 P10 P19 P28 P05)
    (h04 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    : length_sum P30 P10 P00 P09 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0880
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0880

theorem v06_sealed_holdout_0881
    (P01 P02 P05 P11 P12 P15 P16 P20 P22 P23 P27 P28 P29 P30 : Point)
    (L12 : Line)
    (h00 : equal_length P29 P20 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : midpoint P28 P29 P30)
    (h03 : angle_bisector_line P12 P29 P16 P27 L12)
    (h04 : area_le P02 P23 P12 P01 P22 P11)
    : equal_length P29 P20 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0881
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0881

theorem v06_sealed_holdout_0882
    (P00 P02 P03 P06 P07 P09 P12 P13 P18 P19 P22 P23 P24 P25 P26 : Point)
    (C02 C22 : Circle)
    (h00 : area_eq P18 P23 P22 P02 P12 P24)
    (h01 : area_eq P02 P12 P24 P03 P13 P25)
    (h02 : midpoint P03 P06 P09)
    (h03 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    (h04 : circle_circle_intersection P19 C22 C02)
    : area_eq P18 P23 P22 P03 P13 P25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0882
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0882

theorem v06_sealed_holdout_0883
    (P02 P05 P09 P11 P13 P15 P16 P20 P24 P26 P27 P28 P31 : Point)
    (L08 : Line)
    (h00 : equal_length P31 P20 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : angle_bisector_line P09 P26 P16 P27 L08)
    (h03 : directed_angle_eq_mod_pi P13 P28 P11 P26 P09 P24)
    (h04 : between P16 P09 P02)
    : equal_length P31 P20 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0883
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0883

theorem v06_sealed_holdout_0884
    (P03 P04 P05 P07 P08 P09 P13 P18 P19 P20 P21 P22 P23 P24 P25 P26 P30 P31 : Point)
    (L20 : Line)
    (C02 C22 : Circle)
    (h00 : angle_bisector_line P21 P05 P25 P03 L20)
    (h01 : circle_circle_intersection P19 C22 C02)
    (h02 : directed_angle_eq_mod_pi P20 P05 P22 P07 P24 P09)
    (h03 : area_le P23 P18 P13 P08 P03 P30)
    (h04 : between P26 P31 P04)
    : angle_bisector P21 P05 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0884
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0884

theorem v06_sealed_holdout_0885
    (P01 P03 P05 P06 P10 P16 P17 P18 P19 P20 P21 P24 P27 P28 P29 P30 : Point)
    (L18 L28 : Line)
    (h00 : angle_bisector_line P17 P06 P24 P03 L18)
    (h01 : area_le P21 P20 P19 P18 P17 P16)
    (h02 : area_le P24 P01 P10 P19 P28 P05)
    (h03 : angle_bisector_line P16 P29 P17 P27 L28)
    (h04 : midpoint P30 P27 P24)
    : angle_bisector P17 P06 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0885
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0885

theorem v06_sealed_holdout_0886
    (P00 P02 P03 P04 P05 P07 P10 P11 P12 P13 P15 P16 P21 P22 P23 P24 P26 P31 : Point)
    (h00 : directed_angle_eq_mod_pi P26 P13 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : area_le P31 P10 P21 P00 P11 P22)
    (h03 : between P02 P23 P12)
    (h04 : between P05 P04 P03)
    : directed_angle_eq_mod_pi P26 P13 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0886
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0886

theorem v06_sealed_holdout_0887
    (P00 P02 P03 P05 P07 P09 P10 P12 P13 P14 P15 P16 P17 P21 P23 P25 P28 P30 : Point)
    (C18 C26 : Circle)
    (h00 : directed_angle_eq_mod_2pi P15 P16 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P17 P25 P02)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h04 : area_le P12 P13 P14 P15 P16 P17)
    : directed_angle_eq_mod_2pi P15 P16 P10 P17 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0887
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0887

theorem v06_sealed_holdout_0888
    (P03 P04 P07 P09 P11 P13 P15 P16 P19 P22 P23 P24 P25 P26 P28 P31 : Point)
    (C02 C18 : Circle)
    (h00 : directed_angle_eq_mod_pi P28 P13 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : area_le P13 P28 P11 P26 P09 P24)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : midpoint P19 P22 P25)
    : directed_angle_eq_mod_pi P28 P13 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0888
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0888

theorem v06_sealed_holdout_0889
    (P02 P03 P05 P07 P10 P16 P17 P18 P20 P21 P22 P25 P27 P29 P30 : Point)
    (L12 : Line)
    (C10 C18 : Circle)
    (h00 : directed_angle_eq_mod_2pi P17 P16 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P18 P25 P02)
    (h02 : midpoint P20 P05 P22)
    (h03 : angle_bisector_line P20 P29 P16 P27 L12)
    (h04 : circle_circle_intersection P03 C10 C18)
    : directed_angle_eq_mod_2pi P17 P16 P10 P18 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0889
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0889

theorem v06_sealed_holdout_0890
    (P01 P03 P06 P08 P15 P16 P18 P19 P21 P24 P27 P30 : Point)
    (C02 C05 C18 C30 : Circle)
    (h00 : circle_through_three_noncollinear_points P06 P27 P16 C05)
    (h01 : circle_circle_intersection P03 C02 C18)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    (h04 : between P01 P08 P15)
    : triangle_pred P06 P27 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0890
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0890

theorem v06_sealed_holdout_0891
    (P00 P01 P02 P03 P04 P05 P06 P11 P12 P16 P19 P22 P23 P27 P28 : Point)
    (L00 L26 : Line)
    (C20 : Circle)
    (h00 : equilateral P27 P28 P06)
    (h01 : line_circle_intersection P19 L26 C20)
    (h02 : directed_angle_eq_mod_pi P02 P23 P12 P01 P22 P11)
    (h03 : area_le P05 P04 P03 P02 P01 P00)
    (h04 : angle_bisector_line P27 P00 P16 P28 L00)
    : triangle_pred P27 P28 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0891
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0891

theorem v06_sealed_holdout_0892
    (P00 P05 P08 P09 P12 P13 P14 P16 P19 P23 P27 P28 : Point)
    (L24 : Line)
    (C02 C14 C19 : Circle)
    (h00 : circle_through_three_noncollinear_points P08 P27 P16 C19)
    (h01 : angle_bisector_line P13 P23 P16 P27 L24)
    (h02 : area_le P09 P00 P23 P14 P05 P28)
    (h03 : between P12 P13 P14)
    (h04 : circle_circle_intersection P19 C14 C02)
    : triangle_pred P08 P27 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0892
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0892

theorem v06_sealed_holdout_0893
    (P03 P06 P09 P10 P11 P13 P16 P22 P23 P24 P26 P27 P28 P29 : Point)
    (L28 : Line)
    (C02 C18 : Circle)
    (h00 : equilateral P29 P27 P06)
    (h01 : area_le P13 P28 P11 P26 P09 P24)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : angle_bisector_line P24 P29 P16 P27 L28)
    (h04 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    : triangle_pred P29 P27 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0893
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0893

theorem v06_sealed_holdout_0894
    (P03 P04 P06 P08 P10 P12 P13 P18 P23 P25 P26 P27 P29 P30 P31 : Point)
    (C18 C19 : Circle)
    (h00 : equilateral P30 P27 P06)
    (h01 : circle_circle_intersection P03 C18 C19)
    (h02 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    (h03 : between P26 P31 P04)
    (h04 : directed_angle_eq_mod_pi P29 P12 P27 P10 P25 P08)
    : triangle_pred P30 P27 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0894
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0894

theorem v06_sealed_holdout_0895
    (P01 P04 P05 P08 P10 P15 P16 P17 P19 P22 P23 P24 P27 P28 P29 P30 P31 : Point)
    (L16 L28 : Line)
    (RF38 : Reflection)
    (h00 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    (h01 : angle_bisector_line P16 P23 P17 P27 L28)
    (h02 : midpoint P30 P27 P24)
    (h03 : area_le P01 P08 P15 P22 P29 P04)
    (h04 : angle_bisector_line P31 P01 P16 P27 L16)
    : reflection_image RF38 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0895
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0895

theorem v06_sealed_holdout_0896
    (P00 P01 P03 P04 P05 P10 P16 P17 P21 P23 P27 P28 P29 P31 : Point)
    (L00 L08 L28 : Line)
    (HOM07 : Homothety)
    (h00 : between P31 P10 P21)
    (h01 : angle_bisector_line P17 P23 P16 P27 L08)
    (h02 : midpoint P05 P04 P03)
    (h03 : angle_bisector_line P27 P29 P16 P28 L00)
    (h04 : angle_bisector_line P00 P01 P16 P27 L28)
    : homothety_image HOM07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0896
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0896

theorem v06_sealed_holdout_0897
    (P00 P03 P05 P06 P07 P12 P13 P14 P15 P16 P17 P18 P19 P23 P26 P27 : Point)
    (L02 L20 : Line)
    (C06 : Circle)
    (INV44 : Inversion)
    (h00 : area_le P06 P19 P00 P13 P26 P07)
    (h01 : angle_bisector_line P18 P23 P16 P27 L20)
    (h02 : area_le P12 P13 P14 P15 P16 P17)
    (h03 : area_le P15 P26 P05 P16 P27 P06)
    (h04 : line_circle_intersection P03 L02 C06)
    : inversion_image INV44 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0897
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0897

theorem v06_sealed_holdout_0898
    (P02 P03 P10 P16 P19 P22 P23 P25 P28 P29 P31 : Point)
    (L10 L18 : Line)
    (C02 C06 C16 C26 : Circle)
    (SP21 : SpiralSimilarity)
    (h00 : circle_circle_intersection P19 C06 C02)
    (h01 : line_circle_intersection P03 L18 C26)
    (h02 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    (h03 : area_le P22 P03 P16 P29 P10 P23)
    (h04 : line_circle_intersection P19 L10 C16)
    : spiral_similarity_center SP21 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0898
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0898

theorem v06_sealed_holdout_0899
    (P00 P04 P08 P11 P18 P19 P23 P25 P27 P28 P29 P31 : Point)
    (L10 : Line)
    (C08 : Circle)
    (h00 : P23 = P08)
    (h01 : P27 = P19)
    (h02 : P28 = P31)
    (h03 : line_circle_intersection P19 L10 C08)
    (h04 : area_le P00 P25 P18 P11 P04 P29)
    : rotation_preserves_collinear P23 P27 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0899
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0899

theorem v06_sealed_holdout_0900
    (P00 P03 P04 P06 P13 P19 P21 : Point)
    (L02 L10 : Line)
    (C00 C02 C14 C19 : Circle)
    (h00 : circle_with_center_through_point P00 P13 C19)
    (h01 : line_circle_intersection P03 L02 C14)
    (h02 : line_circle_intersection P19 L10 C00)
    (h03 : between P04 P21 P06)
    (h04 : circle_circle_intersection P19 C14 C02)
    : on_circle P13 C19 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0900
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0900

theorem v06_sealed_holdout_0901
    (P03 P04 P08 P10 P11 P12 P14 P17 P19 P21 P23 P26 P30 : Point)
    (L10 L21 : Line)
    (C00 C07 : Circle)
    (h00 : line_circle_intersection P30 L21 C07)
    (h01 : area_le P08 P17 P26 P03 P12 P21)
    (h02 : area_le P11 P30 P17 P04 P23 P10)
    (h03 : between P14 P11 P08)
    (h04 : line_circle_intersection P19 L10 C00)
    : on_circle P30 C07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0901
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0901

theorem v06_sealed_holdout_0902
    (P01 P07 P08 P10 P16 P17 P18 P19 P20 P21 P24 P28 : Point)
    (L30 : Line)
    (C02 C26 C30 : Circle)
    (h00 : tangent_chord_angle P08 P19 P28 L30 C26)
    (h01 : midpoint P18 P07 P28)
    (h02 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    (h03 : between P24 P01 P10)
    (h04 : circle_circle_intersection P19 C30 C02)
    : on_circle P28 C26 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0902
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0902

theorem v06_sealed_holdout_0903
    (P02 P07 P10 P12 P16 P17 P18 P21 P23 P25 P28 P30 P31 : Point)
    (L16 L19 : Line)
    (C04 : Circle)
    (h00 : line_circle_intersection P17 L19 C04)
    (h01 : area_le P25 P16 P07 P30 P21 P12)
    (h02 : angle_bisector_line P07 P25 P18 P28 L16)
    (h03 : midpoint P31 P10 P21)
    (h04 : between P02 P23 P12)
    : on_line P17 L19 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0903
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0903

theorem v06_sealed_holdout_0904
    (P00 P03 P06 P09 P12 P14 P15 P18 P19 P23 P25 P29 : Point)
    (L10 L11 : Line)
    (C16 C18 C26 : Circle)
    (h00 : altitude P06 P29 P14 P23 L11)
    (h01 : midpoint P00 P25 P18)
    (h02 : area_le P03 P06 P09 P12 P15 P18)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : line_circle_intersection P19 L10 C16)
    : on_line P14 L11 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0904
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0904

theorem v06_sealed_holdout_0905
    (P02 P03 P04 P06 P07 P08 P13 P14 P19 P21 P23 P24 P25 P29 P30 : Point)
    (L02 L05 : Line)
    (C02 C06 C22 : Circle)
    (h00 : altitude P02 P30 P13 P23 L05)
    (h01 : area_le P04 P21 P06 P23 P08 P25)
    (h02 : area_le P07 P02 P29 P24 P19 P14)
    (h03 : line_circle_intersection P03 L02 C22)
    (h04 : circle_circle_intersection P19 C06 C02)
    : on_line P13 L05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0905
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0905

theorem v06_sealed_holdout_0906
    (P03 P05 P07 P09 P10 P13 P18 P20 P22 P23 P24 P25 P28 : Point)
    (L00 L02 L20 : Line)
    (C14 C28 : Circle)
    (h00 : line_circle_intersection P20 L00 C28)
    (h01 : line_circle_intersection P03 L02 C14)
    (h02 : angle_bisector_line P10 P25 P18 P28 L20)
    (h03 : area_le P20 P05 P22 P07 P24 P09)
    (h04 : midpoint P23 P18 P13)
    : on_line P20 L00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0906
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0906

theorem v06_sealed_holdout_0907
    (P03 P16 P17 P18 P19 P20 P21 : Point)
    (L02 L18 L26 L30 : Line)
    (C06 C10 C28 : Circle)
    (h00 : line_circle_intersection P16 L30 C28)
    (h01 : line_circle_intersection P03 L02 C06)
    (h02 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    (h03 : line_circle_intersection P03 L18 C10)
    (h04 : line_circle_intersection P19 L26 C28)
    : on_line P16 L30 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0907
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0907

theorem v06_sealed_holdout_0908
    (P00 P01 P02 P03 P07 P10 P11 P12 P16 P21 P22 P23 P25 P29 P30 P31 : Point)
    (C18 C19 : Circle)
    (h00 : equilateral P29 P23 P01)
    (h01 : area_le P25 P16 P07 P30 P21 P12)
    (h02 : circle_circle_intersection P03 C18 C19)
    (h03 : area_le P31 P10 P21 P00 P11 P22)
    (h04 : area_le P02 P23 P12 P01 P22 P11)
    : equal_length P29 P23 P23 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0908
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0908

theorem v06_sealed_holdout_0909
    (P00 P03 P08 P10 P12 P18 P19 P24 P25 P27 P29 : Point)
    (C02 C18 C26 C30 : Circle)
    (h00 : equilateral P25 P24 P00)
    (h01 : area_le P29 P12 P27 P10 P25 P08)
    (h02 : midpoint P00 P25 P18)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : circle_circle_intersection P03 C26 C18)
    : equal_length P25 P24 P24 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0909
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0909

theorem v06_sealed_holdout_0910
    (P03 P09 P10 P15 P16 P19 P20 P23 P30 P31 : Point)
    (L18 L26 : Line)
    (C02 C04 C06 C18 : Circle)
    (h00 : length_sum P30 P10 P31 P09 P16 P23)
    (h01 : line_circle_intersection P03 L18 C18)
    (h02 : line_circle_intersection P19 L26 C04)
    (h03 : midpoint P10 P15 P20)
    (h04 : circle_circle_intersection P19 C06 C02)
    : length_sum P31 P09 P30 P10 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0910
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0910

theorem v06_sealed_holdout_0911
    (P01 P05 P08 P11 P14 P15 P16 P17 P20 P24 P27 P28 P31 : Point)
    (L16 : Line)
    (h00 : equal_length P27 P20 P16 P28)
    (h01 : equal_length P16 P28 P05 P15)
    (h02 : midpoint P14 P11 P08)
    (h03 : between P17 P24 P31)
    (h04 : angle_bisector_line P15 P01 P16 P27 L16)
    : equal_length P27 P20 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0911
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0911

theorem v06_sealed_holdout_0912
    (P01 P02 P03 P06 P07 P12 P13 P14 P16 P20 P22 P23 P24 P25 P26 P27 P28 : Point)
    (L04 : Line)
    (C02 C18 : Circle)
    (h00 : area_eq P16 P24 P22 P02 P12 P23)
    (h01 : area_eq P02 P12 P23 P03 P13 P25)
    (h02 : angle_bisector_line P06 P27 P16 P28 L04)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    : area_eq P16 P24 P22 P03 P13 P25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0912
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0912

theorem v06_sealed_holdout_0913
    (P00 P01 P03 P05 P15 P16 P19 P21 P27 P28 P29 P30 P31 : Point)
    (C02 C10 C14 C18 : Circle)
    (h00 : equal_length P29 P21 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    (h03 : circle_circle_intersection P19 C14 C02)
    (h04 : circle_circle_intersection P03 C10 C18)
    : equal_length P29 P21 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0913
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0913

theorem v06_sealed_holdout_0914
    (P00 P03 P06 P09 P12 P13 P14 P19 P23 P25 : Point)
    (L02 L22 L26 : Line)
    (C12 C30 : Circle)
    (h00 : angle_bisector_line P19 P06 P25 P03 L22)
    (h01 : line_circle_intersection P19 L26 C12)
    (h02 : line_circle_intersection P03 L02 C30)
    (h03 : midpoint P09 P00 P23)
    (h04 : midpoint P12 P13 P14)
    : angle_bisector P19 P06 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0914
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0914

theorem v06_sealed_holdout_0915
    (P02 P03 P06 P09 P11 P13 P15 P16 P19 P24 P27 P28 : Point)
    (L08 L20 : Line)
    (C02 C14 : Circle)
    (h00 : angle_bisector_line P15 P06 P24 P03 L20)
    (h01 : circle_circle_intersection P19 C14 C02)
    (h02 : angle_bisector_line P09 P27 P16 P28 L08)
    (h03 : midpoint P13 P28 P11)
    (h04 : midpoint P16 P09 P02)
    : angle_bisector P15 P06 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0915
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0915

theorem v06_sealed_holdout_0916
    (P01 P03 P04 P07 P14 P15 P16 P19 P20 P23 P24 P25 P27 P31 : Point)
    (L10 L12 : Line)
    (C00 C18 C19 : Circle)
    (h00 : directed_angle_eq_mod_pi P24 P14 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P25)
    (h02 : line_circle_intersection P19 L10 C00)
    (h03 : circle_circle_intersection P03 C18 C19)
    (h04 : angle_bisector_line P20 P01 P16 P27 L12)
    : directed_angle_eq_mod_pi P24 P14 P04 P07 P16 P25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0916
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0916

theorem v06_sealed_holdout_0917
    (P01 P02 P05 P07 P10 P13 P16 P17 P19 P21 P24 P25 P27 P28 P30 : Point)
    (L28 : Line)
    (h00 : directed_angle_eq_mod_2pi P13 P17 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    (h03 : angle_bisector_line P16 P30 P17 P27 L28)
    (h04 : midpoint P30 P27 P24)
    : directed_angle_eq_mod_2pi P13 P17 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0917
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0917

theorem v06_sealed_holdout_0918
    (P00 P01 P04 P07 P10 P11 P14 P15 P16 P17 P21 P22 P23 P24 P26 P27 P30 P31 : Point)
    (L04 L08 : Line)
    (h00 : directed_angle_eq_mod_pi P26 P14 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    (h03 : angle_bisector_line P17 P30 P16 P27 L08)
    (h04 : angle_bisector_line P22 P01 P16 P27 L04)
    : directed_angle_eq_mod_pi P26 P14 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0918
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0918

theorem v06_sealed_holdout_0919
    (P00 P02 P03 P05 P07 P09 P10 P14 P15 P16 P17 P21 P23 P25 P28 P30 : Point)
    (C18 C19 C26 : Circle)
    (h00 : directed_angle_eq_mod_2pi P15 P17 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h04 : circle_circle_intersection P03 C18 C19)
    : directed_angle_eq_mod_2pi P15 P17 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0919
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0919

theorem v06_sealed_holdout_0920
    (P01 P03 P04 P16 P19 P24 P27 P28 : Point)
    (L28 : Line)
    (C02 C06 C10 C18 C23 : Circle)
    (h00 : circle_through_three_noncollinear_points P04 P28 P16 C23)
    (h01 : circle_circle_intersection P03 C10 C18)
    (h02 : circle_circle_intersection P19 C06 C02)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : angle_bisector_line P24 P01 P16 P27 L28)
    : triangle_pred P04 P28 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0920
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0920

theorem v06_sealed_holdout_0921
    (P03 P04 P06 P08 P13 P17 P18 P20 P23 P24 P25 P26 P28 P30 P31 : Point)
    (C18 C19 : Circle)
    (h00 : equilateral P25 P28 P06)
    (h01 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    (h02 : circle_circle_intersection P03 C18 C19)
    (h03 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    (h04 : midpoint P26 P31 P04)
    : triangle_pred P25 P28 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0921
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0921

theorem v06_sealed_holdout_0922
    (P01 P04 P05 P06 P08 P10 P15 P16 P19 P22 P24 P27 P28 P29 P30 : Point)
    (L26 : Line)
    (C05 C28 : Circle)
    (h00 : circle_through_three_noncollinear_points P06 P28 P16 C05)
    (h01 : area_le P24 P01 P10 P19 P28 P05)
    (h02 : line_circle_intersection P19 L26 C28)
    (h03 : midpoint P30 P27 P24)
    (h04 : directed_angle_eq_mod_pi P01 P08 P15 P22 P29 P04)
    : triangle_pred P06 P28 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0922
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0922

theorem v06_sealed_holdout_0923
    (P00 P03 P04 P07 P10 P11 P17 P19 P23 P27 P30 : Point)
    (L02 L18 : Line)
    (C02 C06 C10 : Circle)
    (h00 : equilateral P00 P27 P07)
    (h01 : line_circle_intersection P03 L02 C06)
    (h02 : circle_circle_intersection P19 C06 C02)
    (h03 : line_circle_intersection P03 L18 C10)
    (h04 : area_le P11 P30 P17 P04 P23 P10)
    : triangle_pred P00 P27 P07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0923
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0923

theorem v06_sealed_holdout_0924
    (P01 P03 P06 P16 P19 P27 P28 P29 : Point)
    (L12 L18 : Line)
    (C02 C18 C22 C26 : Circle)
    (h00 : equilateral P28 P29 P06)
    (h01 : circle_circle_intersection P03 C26 C18)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : line_circle_intersection P03 L18 C02)
    (h04 : angle_bisector_line P28 P01 P16 P27 L12)
    : triangle_pred P28 P29 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0924
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0924

theorem v06_sealed_holdout_0925
    (P02 P03 P09 P11 P13 P16 P19 P22 P24 P25 P26 P28 : Point)
    (L02 : Line)
    (C18 C22 C26 : Circle)
    (RF56 : Reflection)
    (h00 : line_circle_intersection P03 L02 C22)
    (h01 : area_le P13 P28 P11 P26 P09 P24)
    (h02 : midpoint P16 P09 P02)
    (h03 : between P19 P22 P25)
    (h04 : circle_circle_intersection P03 C26 C18)
    : reflection_image RF56 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0925
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0925

theorem v06_sealed_holdout_0926
    (P03 P04 P17 P19 P24 P26 P31 : Point)
    (L18 L26 : Line)
    (C02 C04 C06 C18 : Circle)
    (HOM21 : Homothety)
    (h00 : midpoint P17 P24 P31)
    (h01 : line_circle_intersection P03 L18 C18)
    (h02 : line_circle_intersection P19 L26 C04)
    (h03 : midpoint P26 P31 P04)
    (h04 : circle_circle_intersection P19 C06 C02)
    : homothety_image HOM21 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0926
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0926

theorem v06_sealed_holdout_0927
    (P01 P03 P08 P10 P14 P15 P24 P27 P30 : Point)
    (L18 : Line)
    (C18 : Circle)
    (INV54 : Inversion)
    (h00 : midpoint P24 P01 P10)
    (h01 : midpoint P27 P14 P01)
    (h02 : midpoint P30 P27 P24)
    (h03 : midpoint P01 P08 P15)
    (h04 : line_circle_intersection P03 L18 C18)
    : inversion_image INV54 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0927
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0927

theorem v06_sealed_holdout_0928
    (P00 P02 P03 P10 P11 P12 P16 P19 P21 P22 P23 P27 P31 : Point)
    (L10 L18 L28 : Line)
    (C10 C24 : Circle)
    (SP27 : SpiralSimilarity)
    (h00 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    (h01 : between P02 P23 P12)
    (h02 : line_circle_intersection P19 L10 C24)
    (h03 : line_circle_intersection P03 L18 C10)
    (h04 : angle_bisector_line P00 P02 P16 P27 L28)
    : spiral_similarity_center SP27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0928
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0928

theorem v06_sealed_holdout_0929
    (P05 P06 P07 P08 P15 P16 P18 P19 P21 P26 P27 P28 P29 P31 : Point)
    (h00 : P21 = P08)
    (h01 : P28 = P19)
    (h02 : P29 = P31)
    (h03 : area_le P15 P26 P05 P16 P27 P06)
    (h04 : between P18 P07 P28)
    : rotation_preserves_collinear P21 P28 P29 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0929
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0929

theorem v06_sealed_holdout_0930
    (P03 P07 P12 P16 P17 P21 P23 P24 P25 P28 P29 P30 P31 : Point)
    (L02 L28 : Line)
    (C13 C30 : Circle)
    (h00 : circle_through_three_noncollinear_points P23 P17 P31 C13)
    (h01 : angle_bisector_line P24 P23 P17 P28 L28)
    (h02 : line_circle_intersection P03 L02 C30)
    (h03 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h04 : midpoint P28 P29 P30)
    : on_circle P23 C13 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0930
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0930

theorem v06_sealed_holdout_0931
    (P03 P08 P10 P12 P17 P19 P23 P25 P27 P28 P29 P30 : Point)
    (L00 L08 L21 : Line)
    (C02 C21 C30 : Circle)
    (h00 : line_circle_intersection P28 L21 C21)
    (h01 : angle_bisector_line P25 P23 P17 P28 L08)
    (h02 : area_le P29 P12 P27 P10 P25 P08)
    (h03 : angle_bisector_line P03 P30 P17 P28 L00)
    (h04 : circle_circle_intersection P19 C30 C02)
    : on_circle P28 C21 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0931
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0931

theorem v06_sealed_holdout_0932
    (P01 P02 P07 P08 P09 P13 P15 P17 P25 P27 P28 P29 P31 : Point)
    (L08 L16 : Line)
    (C12 : Circle)
    (h00 : chord P25 P13 C12)
    (h01 : between P01 P08 P15)
    (h02 : angle_bisector_line P31 P27 P17 P28 L16)
    (h03 : between P07 P02 P29)
    (h04 : angle_bisector_line P09 P01 P17 P28 L08)
    : on_circle P25 C12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0932
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0932

theorem v06_sealed_holdout_0933
    (P03 P04 P10 P11 P15 P17 P23 P24 P30 P31 : Point)
    (L18 L21 : Line)
    (C18 C20 C26 : Circle)
    (h00 : line_circle_intersection P15 L21 C20)
    (h01 : area_le P11 P30 P17 P04 P23 P10)
    (h02 : circle_circle_intersection P03 C26 C18)
    (h03 : midpoint P17 P24 P31)
    (h04 : line_circle_intersection P03 L18 C18)
    : on_line P15 L21 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0933
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0933

theorem v06_sealed_holdout_0934
    (P01 P05 P07 P10 P14 P19 P20 P21 P24 P26 P27 P28 P29 P30 : Point)
    (L20 : Line)
    (h00 : angle_bisector_line P29 P01 P21 P30 L20)
    (h01 : between P21 P20 P19)
    (h02 : area_le P24 P01 P10 P19 P28 P05)
    (h03 : area_le P27 P14 P01 P20 P07 P26)
    (h04 : between P30 P27 P24)
    : on_line P29 L20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0934
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0934

theorem v06_sealed_holdout_0935
    (P02 P07 P12 P16 P19 P20 P23 P25 P28 P29 P30 : Point)
    (L16 L26 : Line)
    (C20 : Circle)
    (h00 : angle_bisector_line P25 P02 P20 P29 L16)
    (h01 : between P25 P16 P07)
    (h02 : between P28 P29 P30)
    (h03 : line_circle_intersection P19 L26 C20)
    (h04 : midpoint P02 P23 P12)
    : on_line P25 L16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0935
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0935

theorem v06_sealed_holdout_0936
    (P00 P03 P06 P09 P19 P21 P29 : Point)
    (L12 : Line)
    (C02 C06 C18 : Circle)
    (h00 : angle_bisector_line P21 P03 P19 P29 L12)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : midpoint P03 P06 P09)
    (h04 : between P06 P19 P00)
    : on_line P21 L12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0936
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0936

theorem v06_sealed_holdout_0937
    (P02 P03 P07 P10 P14 P15 P17 P19 P20 P24 P25 P28 P29 P30 P31 : Point)
    (L00 L10 L16 : Line)
    (C08 C12 : Circle)
    (h00 : line_circle_intersection P14 L00 C12)
    (h01 : angle_bisector_line P31 P24 P17 P28 L16)
    (h02 : area_le P07 P02 P29 P24 P19 P14)
    (h03 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    (h04 : line_circle_intersection P19 L10 C08)
    : on_line P14 L00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0937
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0937

theorem v06_sealed_holdout_0938
    (P01 P04 P05 P08 P10 P11 P14 P17 P19 P20 P22 P23 P24 P27 P30 : Point)
    (L10 : Line)
    (C00 : Circle)
    (h00 : equilateral P27 P24 P01)
    (h01 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h02 : midpoint P14 P11 P08)
    (h03 : line_circle_intersection P19 L10 C00)
    (h04 : between P20 P05 P22)
    : equal_length P27 P24 P24 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0938
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0938

theorem v06_sealed_holdout_0939
    (P00 P01 P03 P10 P19 P23 P24 P25 : Point)
    (C02 C06 C10 C14 C18 : Circle)
    (h00 : equilateral P23 P25 P00)
    (h01 : circle_circle_intersection P19 C14 C02)
    (h02 : circle_circle_intersection P03 C10 C18)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : midpoint P24 P01 P10)
    : equal_length P23 P25 P25 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0939
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0939

theorem v06_sealed_holdout_0940
    (P03 P09 P10 P11 P16 P19 P21 P23 P28 P30 P31 : Point)
    (L02 L10 L18 : Line)
    (C02 C16 C30 : Circle)
    (h00 : length_sum P28 P11 P30 P09 P16 P23)
    (h01 : line_circle_intersection P03 L02 C30)
    (h02 : line_circle_intersection P19 L10 C16)
    (h03 : line_circle_intersection P03 L18 C02)
    (h04 : between P31 P10 P21)
    : length_sum P30 P09 P28 P11 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0940
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0940

theorem v06_sealed_holdout_0941
    (P00 P05 P06 P07 P13 P15 P16 P18 P19 P21 P25 P26 P27 : Point)
    (L26 : Line)
    (C12 : Circle)
    (h00 : equal_length P25 P21 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : midpoint P00 P25 P18)
    (h03 : line_circle_intersection P19 L26 C12)
    (h04 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    : equal_length P25 P21 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0941
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0941

theorem v06_sealed_holdout_0942
    (P02 P03 P07 P10 P12 P13 P14 P15 P16 P19 P20 P22 P23 P24 P25 P27 P29 P30 : Point)
    (L04 : Line)
    (h00 : area_eq P14 P25 P22 P02 P12 P23)
    (h01 : area_eq P02 P12 P23 P03 P13 P24)
    (h02 : area_le P07 P02 P29 P24 P19 P14)
    (h03 : area_le P10 P15 P20 P25 P30 P03)
    (h04 : angle_bisector_line P14 P02 P16 P27 L04)
    : area_eq P14 P25 P22 P03 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0942
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0942

theorem v06_sealed_holdout_0943
    (P03 P05 P08 P11 P14 P15 P16 P17 P21 P24 P27 P28 P31 : Point)
    (C18 C19 : Circle)
    (h00 : equal_length P27 P21 P16 P28)
    (h01 : equal_length P16 P28 P05 P15)
    (h02 : between P14 P11 P08)
    (h03 : between P17 P24 P31)
    (h04 : circle_circle_intersection P03 C18 C19)
    : equal_length P27 P21 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0943
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0943

theorem v06_sealed_holdout_0944
    (P03 P07 P16 P17 P18 P19 P20 P21 P25 P28 P30 : Point)
    (L02 L24 L28 : Line)
    (C02 C14 C18 : Circle)
    (h00 : angle_bisector_line P17 P07 P25 P03 L24)
    (h01 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : angle_bisector_line P16 P30 P17 P28 L28)
    (h04 : line_circle_intersection P03 L02 C14)
    : angle_bisector P17 P07 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0944
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0944

theorem v06_sealed_holdout_0945
    (P00 P01 P02 P03 P07 P10 P11 P12 P13 P16 P21 P22 P23 P24 P25 P28 P29 P30 P31 : Point)
    (L22 : Line)
    (h00 : angle_bisector_line P13 P07 P24 P03 L22)
    (h01 : area_le P25 P16 P07 P30 P21 P12)
    (h02 : area_le P28 P29 P30 P31 P00 P01)
    (h03 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    (h04 : directed_angle_eq_mod_pi P02 P23 P12 P01 P22 P11)
    : angle_bisector P13 P07 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0945
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0945

theorem v06_sealed_holdout_0946
    (P00 P03 P04 P05 P06 P07 P09 P14 P15 P16 P22 P23 P24 P28 P31 : Point)
    (C18 C26 : Circle)
    (h00 : directed_angle_eq_mod_pi P22 P14 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : between P03 P06 P09)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : area_le P09 P00 P23 P14 P05 P28)
    : directed_angle_eq_mod_pi P22 P14 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0946
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0946

theorem v06_sealed_holdout_0947
    (P02 P03 P07 P09 P10 P11 P13 P15 P16 P18 P20 P21 P24 P25 P26 P28 P30 : Point)
    (h00 : directed_angle_eq_mod_2pi P11 P18 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    (h03 : directed_angle_eq_mod_pi P13 P28 P11 P26 P09 P24)
    (h04 : midpoint P16 P09 P02)
    : directed_angle_eq_mod_2pi P11 P18 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0947
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0947

theorem v06_sealed_holdout_0948
    (P03 P04 P07 P08 P13 P15 P16 P17 P18 P19 P23 P24 P25 P27 P30 P31 : Point)
    (L16 : Line)
    (C02 C22 : Circle)
    (h00 : directed_angle_eq_mod_pi P24 P15 P04 P16 P23 P31)
    (h01 : directed_angle_eq_mod_pi P16 P23 P31 P07 P17 P25)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : angle_bisector_line P15 P31 P16 P27 L16)
    (h04 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    : directed_angle_eq_mod_pi P24 P15 P04 P07 P17 P25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0948
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0948

theorem v06_sealed_holdout_0949
    (P01 P02 P07 P10 P13 P14 P15 P16 P18 P21 P24 P25 P27 P30 : Point)
    (h00 : directed_angle_eq_mod_2pi P13 P18 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : between P24 P01 P10)
    (h03 : between P27 P14 P01)
    (h04 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    : directed_angle_eq_mod_2pi P13 P18 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0949
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0949

theorem v06_sealed_holdout_0950
    (P02 P16 P17 P19 P27 P28 P29 P30 P31 : Point)
    (L08 L10 : Line)
    (C02 C09 C14 C24 : Circle)
    (h00 : circle_through_three_noncollinear_points P02 P29 P16 C09)
    (h01 : midpoint P28 P29 P30)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : angle_bisector_line P17 P31 P16 P27 L08)
    (h04 : line_circle_intersection P19 L10 C24)
    : triangle_pred P02 P29 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0950
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0950

theorem v06_sealed_holdout_0951
    (P00 P03 P05 P06 P09 P12 P13 P14 P16 P23 P27 P28 P29 : Point)
    (L24 : Line)
    (h00 : equilateral P23 P29 P06)
    (h01 : between P03 P06 P09)
    (h02 : angle_bisector_line P13 P28 P16 P27 L24)
    (h03 : area_le P09 P00 P23 P14 P05 P28)
    (h04 : between P12 P13 P14)
    : triangle_pred P23 P29 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0951
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0951

theorem v06_sealed_holdout_0952
    (P02 P04 P09 P10 P11 P13 P15 P16 P19 P20 P22 P25 P27 P28 P29 : Point)
    (C23 : Circle)
    (h00 : circle_through_three_noncollinear_points P04 P29 P16 C23)
    (h01 : midpoint P10 P15 P20)
    (h02 : between P13 P28 P11)
    (h03 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    (h04 : midpoint P19 P22 P25)
    : triangle_pred P04 P29 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0952
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0952

theorem v06_sealed_holdout_0953
    (P02 P03 P05 P06 P08 P13 P16 P17 P18 P20 P22 P23 P24 P25 P27 P29 P30 P31 : Point)
    (L08 : Line)
    (h00 : equilateral P25 P29 P06)
    (h01 : between P17 P24 P31)
    (h02 : midpoint P20 P05 P22)
    (h03 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    (h04 : angle_bisector_line P25 P02 P16 P27 L08)
    : triangle_pred P25 P29 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0953
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0953

theorem v06_sealed_holdout_0954
    (P01 P04 P05 P06 P08 P10 P15 P18 P19 P21 P22 P24 P26 P27 P28 P29 P30 : Point)
    (C02 C30 : Circle)
    (h00 : equilateral P26 P29 P06)
    (h01 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    (h04 : area_le P01 P08 P15 P22 P29 P04)
    : triangle_pred P26 P29 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0954
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0954

theorem v06_sealed_holdout_0955
    (P00 P01 P02 P03 P04 P05 P07 P08 P12 P16 P17 P22 P25 P26 P27 : Point)
    (L12 L16 : Line)
    (C10 C18 : Circle)
    (RF10 : Reflection)
    (h00 : angle_bisector_line P07 P22 P16 P27 L16)
    (h01 : angle_bisector_line P12 P25 P16 P27 L12)
    (h02 : circle_circle_intersection P03 C10 C18)
    (h03 : area_le P05 P04 P03 P02 P01 P00)
    (h04 : between P08 P17 P26)
    : reflection_image RF10 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0955
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0955

theorem v06_sealed_holdout_0956
    (P00 P02 P03 P06 P09 P12 P13 P14 P15 P16 P17 P18 P19 P27 P28 : Point)
    (L12 L20 : Line)
    (HOM35 : Homothety)
    (h00 : directed_angle_eq_mod_pi P03 P06 P09 P12 P15 P18)
    (h01 : midpoint P06 P19 P00)
    (h02 : angle_bisector_line P18 P28 P16 P27 L20)
    (h03 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h04 : angle_bisector_line P28 P02 P16 P27 L12)
    : homothety_image HOM35 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0956
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0956

theorem v06_sealed_holdout_0957
    (P02 P03 P09 P10 P14 P16 P19 P22 P23 P25 P27 P29 : Point)
    (L04 : Line)
    (C10 C18 : Circle)
    (INV00 : Inversion)
    (h00 : circle_circle_intersection P03 C10 C18)
    (h01 : angle_bisector_line P14 P25 P16 P27 L04)
    (h02 : between P16 P09 P02)
    (h03 : between P19 P22 P25)
    (h04 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    : inversion_image INV00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0957
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0957

theorem v06_sealed_holdout_0958
    (P03 P04 P05 P16 P17 P19 P20 P22 P24 P26 P27 P30 P31 : Point)
    (L04 : Line)
    (C02 C14 : Circle)
    (SP33 : SpiralSimilarity)
    (h00 : midpoint P17 P24 P31)
    (h01 : between P20 P05 P22)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : midpoint P26 P31 P04)
    (h04 : angle_bisector_line P30 P03 P16 P27 L04)
    : spiral_similarity_center SP33 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0958
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0958

theorem v06_sealed_holdout_0959
    (P01 P03 P08 P15 P19 P20 P28 P29 P31 : Point)
    (L18 : Line)
    (C18 : Circle)
    (h00 : P19 = P08)
    (h01 : P29 = P20)
    (h02 : P28 = P31)
    (h03 : between P01 P08 P15)
    (h04 : line_circle_intersection P03 L18 C18)
    : rotation_preserves_collinear P19 P29 P28 P08 P20 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0959
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0959

theorem v06_sealed_holdout_0960
    (P03 P04 P05 P11 P15 P17 P28 P30 : Point)
    (C02 C10 C18 C27 : Circle)
    (h00 : circle_with_center_through_point P28 P15 C27)
    (h01 : circle_circle_intersection P03 C10 C18)
    (h02 : midpoint P05 P04 P03)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : midpoint P11 P30 P17)
    : on_circle P15 C27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0960
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0960

theorem v06_sealed_holdout_0961
    (P01 P05 P06 P07 P08 P10 P17 P18 P19 P20 P24 P27 P28 P29 : Point)
    (L02 L26 : Line)
    (C02 C06 C18 C28 : Circle)
    (h00 : tangent_chord_angle P08 P20 P29 L02 C18)
    (h01 : directed_angle_eq_mod_pi P18 P07 P28 P17 P06 P27)
    (h02 : circle_circle_intersection P19 C06 C02)
    (h03 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    (h04 : line_circle_intersection P19 L26 C28)
    : on_circle P29 C18 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0961
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0961

theorem v06_sealed_holdout_0962
    (P00 P01 P03 P04 P07 P12 P16 P18 P21 P22 P25 P28 P29 P30 P31 : Point)
    (L12 L22 : Line)
    (C02 : Circle)
    (h00 : tangent_chord_angle P04 P21 P28 L22 C02)
    (h01 : between P22 P03 P16)
    (h02 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h03 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    (h04 : angle_bisector_line P12 P01 P18 P28 L12)
    : on_circle P28 C02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0962
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0962

theorem v06_sealed_holdout_0963
    (P00 P04 P06 P11 P13 P15 P18 P19 P23 P25 P28 P29 P30 : Point)
    (L10 L24 L26 L29 : Line)
    (C12 C16 : Circle)
    (h00 : altitude P06 P30 P15 P23 L29)
    (h01 : area_le P00 P25 P18 P11 P04 P29)
    (h02 : line_circle_intersection P19 L26 C12)
    (h03 : angle_bisector_line P13 P29 P19 P28 L24)
    (h04 : line_circle_intersection P19 L10 C16)
    : on_line P15 L29 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0963
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0963

theorem v06_sealed_holdout_0964
    (P02 P03 P04 P06 P07 P08 P11 P13 P14 P19 P21 P23 P24 P25 P28 P29 P31 : Point)
    (L23 : Line)
    (C10 C18 : Circle)
    (h00 : altitude P02 P31 P14 P23 L23)
    (h01 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    (h02 : directed_angle_eq_mod_pi P07 P02 P29 P24 P19 P14)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : between P13 P28 P11)
    : on_line P14 L23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0964
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0964

theorem v06_sealed_holdout_0965
    (P00 P03 P05 P07 P09 P19 P20 P22 P24 P28 : Point)
    (L02 L06 L12 : Line)
    (C02 C14 C22 C28 : Circle)
    (h00 : line_circle_intersection P20 L06 C28)
    (h01 : line_circle_intersection P03 L02 C14)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : area_le P20 P05 P22 P07 P24 P09)
    (h04 : angle_bisector_line P20 P00 P19 P28 L12)
    : on_line P20 L06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0965
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0965

theorem v06_sealed_holdout_0966
    (P01 P03 P04 P16 P17 P18 P19 P20 P21 P28 P29 : Point)
    (L08 L16 L26 : Line)
    (C02 C18 C20 : Circle)
    (h00 : angle_bisector_line P19 P04 P20 P29 L16)
    (h01 : line_circle_intersection P19 L26 C20)
    (h02 : angle_bisector_line P01 P28 P17 P29 L08)
    (h03 : area_le P21 P20 P19 P18 P17 P16)
    (h04 : circle_circle_intersection P03 C02 C18)
    : on_line P19 L16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0966
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0966

theorem v06_sealed_holdout_0967
    (P00 P01 P02 P07 P10 P16 P17 P18 P21 P24 P25 P28 P29 P30 P31 : Point)
    (L08 : Line)
    (h00 : equilateral P29 P24 P02)
    (h01 : midpoint P25 P16 P07)
    (h02 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    (h03 : midpoint P31 P10 P21)
    (h04 : angle_bisector_line P17 P01 P18 P28 L08)
    : equal_length P29 P24 P24 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0967
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0967

theorem v06_sealed_holdout_0968
    (P00 P01 P06 P07 P13 P18 P19 P25 P26 : Point)
    (L10 L26 : Line)
    (C08 C12 : Circle)
    (h00 : equilateral P25 P26 P01)
    (h01 : line_circle_intersection P19 L10 C08)
    (h02 : midpoint P00 P25 P18)
    (h03 : line_circle_intersection P19 L26 C12)
    (h04 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    : equal_length P25 P26 P26 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0968
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0968

theorem v06_sealed_holdout_0969
    (P00 P01 P02 P04 P07 P08 P10 P15 P16 P20 P21 P22 P26 P27 P29 P31 : Point)
    (L16 : Line)
    (h00 : equilateral P21 P26 P00)
    (h01 : directed_angle_eq_mod_pi P01 P08 P15 P22 P29 P04)
    (h02 : angle_bisector_line P31 P29 P16 P27 L16)
    (h03 : midpoint P07 P02 P29)
    (h04 : midpoint P10 P15 P20)
    : equal_length P21 P26 P26 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0969
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0969

theorem v06_sealed_holdout_0970
    (P03 P04 P09 P10 P11 P12 P16 P17 P23 P25 P26 P27 P28 P30 : Point)
    (L00 L02 L20 : Line)
    (C14 : Circle)
    (h00 : length_sum P26 P12 P30 P09 P16 P23)
    (h01 : angle_bisector_line P27 P25 P16 P28 L00)
    (h02 : area_le P11 P30 P17 P04 P23 P10)
    (h03 : line_circle_intersection P03 L02 C14)
    (h04 : angle_bisector_line P10 P03 P16 P27 L20)
    : length_sum P30 P09 P26 P12 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0970
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0970

theorem v06_sealed_holdout_0971
    (P01 P03 P05 P10 P15 P16 P17 P18 P19 P20 P21 P22 P23 P24 P27 : Point)
    (C10 C18 : Circle)
    (h00 : equal_length P23 P22 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : circle_circle_intersection P03 C10 C18)
    (h03 : area_le P21 P20 P19 P18 P17 P16)
    (h04 : between P24 P01 P10)
    : equal_length P23 P22 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0971
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0971

theorem v06_sealed_holdout_0972
    (P00 P01 P02 P03 P07 P10 P11 P12 P13 P14 P16 P21 P22 P23 P24 P25 P26 P28 P29 P30 P31 : Point)
    (h00 : area_eq P12 P26 P22 P02 P13 P23)
    (h01 : area_eq P02 P13 P23 P03 P14 P24)
    (h02 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h03 : area_le P28 P29 P30 P31 P00 P01)
    (h04 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    : area_eq P12 P26 P22 P03 P14 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0972
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0972

theorem v06_sealed_holdout_0973
    (P00 P05 P06 P07 P13 P15 P16 P18 P19 P22 P25 P26 P27 : Point)
    (L26 : Line)
    (C12 : Circle)
    (h00 : equal_length P25 P22 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : midpoint P00 P25 P18)
    (h03 : line_circle_intersection P19 L26 C12)
    (h04 : area_le P06 P19 P00 P13 P26 P07)
    : equal_length P25 P22 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0973
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0973

theorem v06_sealed_holdout_0974
    (P02 P03 P07 P15 P17 P19 P25 P28 : Point)
    (L00 L02 L10 L26 : Line)
    (C02 C08 C14 C22 : Circle)
    (h00 : angle_bisector_line P15 P07 P25 P03 L26)
    (h01 : circle_circle_intersection P19 C14 C02)
    (h02 : line_circle_intersection P03 L02 C22)
    (h03 : line_circle_intersection P19 L10 C08)
    (h04 : angle_bisector_line P19 P02 P17 P28 L00)
    : angle_bisector P15 P07 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0974
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0974

theorem v06_sealed_holdout_0975
    (P02 P03 P05 P06 P08 P11 P13 P14 P15 P16 P17 P19 P20 P24 P27 P31 : Point)
    (L16 L24 : Line)
    (C02 C30 : Circle)
    (h00 : angle_bisector_line P11 P08 P24 P03 L24)
    (h01 : circle_circle_intersection P19 C30 C02)
    (h02 : area_le P14 P11 P08 P05 P02 P31)
    (h03 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    (h04 : angle_bisector_line P15 P03 P16 P27 L16)
    : angle_bisector P11 P08 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0975
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0975

theorem v06_sealed_holdout_0976
    (P01 P03 P04 P07 P14 P15 P16 P17 P19 P20 P21 P23 P24 P27 P31 : Point)
    (C02 C18 : Circle)
    (h00 : directed_angle_eq_mod_pi P20 P15 P04 P16 P23 P31)
    (h01 : directed_angle_eq_mod_pi P16 P23 P31 P07 P17 P24)
    (h02 : midpoint P21 P20 P19)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : midpoint P27 P14 P01)
    : directed_angle_eq_mod_pi P20 P15 P04 P07 P17 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0976
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0976

theorem v06_sealed_holdout_0977
    (P02 P07 P09 P10 P12 P16 P19 P21 P23 P25 P27 P29 P30 : Point)
    (L16 L26 : Line)
    (C20 : Circle)
    (h00 : directed_angle_eq_mod_2pi P09 P19 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : angle_bisector_line P07 P29 P16 P27 L16)
    (h03 : line_circle_intersection P19 L26 C20)
    (h04 : midpoint P02 P23 P12)
    : directed_angle_eq_mod_2pi P09 P19 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0977
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0977

theorem v06_sealed_holdout_0978
    (P00 P03 P04 P06 P07 P09 P13 P15 P16 P17 P18 P19 P22 P23 P24 P26 P27 P31 : Point)
    (L20 : Line)
    (h00 : directed_angle_eq_mod_pi P22 P15 P04 P16 P23 P31)
    (h01 : directed_angle_eq_mod_pi P16 P23 P31 P07 P17 P24)
    (h02 : between P03 P06 P09)
    (h03 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    (h04 : angle_bisector_line P18 P03 P16 P27 L20)
    : directed_angle_eq_mod_pi P22 P15 P04 P07 P17 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0978
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0978

theorem v06_sealed_holdout_0979
    (P02 P07 P09 P10 P11 P13 P15 P16 P19 P20 P21 P25 P28 P30 : Point)
    (h00 : directed_angle_eq_mod_2pi P11 P19 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : between P10 P15 P20)
    (h03 : midpoint P13 P28 P11)
    (h04 : between P16 P09 P02)
    : directed_angle_eq_mod_2pi P11 P19 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0979
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0979

theorem v06_sealed_holdout_0980
    (P00 P05 P08 P10 P11 P13 P14 P16 P18 P20 P22 P23 P27 P29 P30 : Point)
    (L20 : Line)
    (C27 : Circle)
    (h00 : circle_through_three_noncollinear_points P00 P30 P16 C27)
    (h01 : between P14 P11 P08)
    (h02 : angle_bisector_line P10 P29 P16 P27 L20)
    (h03 : midpoint P20 P05 P22)
    (h04 : midpoint P23 P18 P13)
    : triangle_pred P00 P30 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0980
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0980

theorem v06_sealed_holdout_0981
    (P01 P03 P05 P06 P10 P14 P19 P21 P24 P27 P28 P30 : Point)
    (C02 C06 C18 C26 : Circle)
    (h00 : equilateral P21 P30 P06)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    (h03 : midpoint P27 P14 P01)
    (h04 : circle_circle_intersection P03 C26 C18)
    : triangle_pred P21 P30 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0981
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0981

theorem v06_sealed_holdout_0982
    (P02 P03 P07 P16 P19 P26 P27 P30 : Point)
    (L02 L10 L16 : Line)
    (C02 C06 C09 C14 C24 : Circle)
    (h00 : circle_through_three_noncollinear_points P02 P30 P16 C09)
    (h01 : angle_bisector_line P07 P26 P16 P27 L16)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : line_circle_intersection P03 L02 C06)
    (h04 : line_circle_intersection P19 L10 C24)
    : triangle_pred P02 P30 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0982
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0982

theorem v06_sealed_holdout_0983
    (P00 P06 P07 P09 P12 P13 P14 P19 P23 P26 P30 : Point)
    (C02 C30 : Circle)
    (h00 : equilateral P23 P30 P06)
    (h01 : circle_circle_intersection P19 C30 C02)
    (h02 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    (h03 : midpoint P09 P00 P23)
    (h04 : between P12 P13 P14)
    : triangle_pred P23 P30 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0983
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0983

theorem v06_sealed_holdout_0984
    (P02 P03 P06 P09 P13 P14 P16 P19 P20 P24 P27 P29 P30 : Point)
    (L02 L04 L26 : Line)
    (C12 C22 : Circle)
    (h00 : equilateral P24 P30 P06)
    (h01 : line_circle_intersection P03 L02 C22)
    (h02 : angle_bisector_line P14 P29 P16 P27 L04)
    (h03 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    (h04 : line_circle_intersection P19 L26 C12)
    : triangle_pred P24 P30 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0984
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0984

theorem v06_sealed_holdout_0985
    (P00 P01 P03 P06 P07 P08 P09 P13 P19 P26 P31 : Point)
    (h00 : P01 = P08)
    (h01 : P26 = P19)
    (h02 : P00 = P31)
    (h03 : midpoint P03 P06 P09)
    (h04 : area_le P06 P19 P00 P13 P26 P07)
    : rotation_preserves_collinear P01 P26 P00 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0985
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0985

theorem v06_sealed_holdout_0986
    (P00 P02 P03 P07 P08 P19 P27 P29 P31 : Point)
    (C10 C18 : Circle)
    (h00 : P29 = P08)
    (h01 : P27 = P19)
    (h02 : P31 = P00)
    (h03 : midpoint P07 P02 P29)
    (h04 : circle_circle_intersection P03 C10 C18)
    : rotation_preserves_collinear P29 P27 P31 P08 P19 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0986
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0986

theorem v06_sealed_holdout_0987
    (P02 P05 P08 P18 P19 P25 P28 P30 P31 : Point)
    (L24 L26 : Line)
    (C28 : Circle)
    (h00 : P25 = P08)
    (h01 : P28 = P19)
    (h02 : P30 = P31)
    (h03 : line_circle_intersection P19 L26 C28)
    (h04 : angle_bisector_line P05 P02 P18 P28 L24)
    : rotation_preserves_collinear P25 P28 P30 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0987
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0987

theorem v06_sealed_holdout_0988
    (P03 P05 P08 P15 P19 P21 P26 P29 P30 P31 : Point)
    (C10 C18 : Circle)
    (h00 : P21 = P08)
    (h01 : P29 = P19)
    (h02 : P30 = P31)
    (h03 : between P15 P26 P05)
    (h04 : circle_circle_intersection P03 C10 C18)
    : rotation_preserves_collinear P21 P29 P30 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0988
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0988

theorem v06_sealed_holdout_0989
    (P02 P03 P08 P10 P16 P17 P19 P22 P23 P25 P28 P29 P30 P31 : Point)
    (h00 : P17 = P08)
    (h01 : P30 = P19)
    (h02 : P28 = P31)
    (h03 : area_le P19 P22 P25 P28 P31 P02)
    (h04 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    : rotation_preserves_collinear P17 P30 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0989
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0989

theorem v06_sealed_holdout_0990
    (P03 P04 P08 P13 P16 P18 P19 P23 P26 P30 P31 : Point)
    (L10 L18 : Line)
    (C08 C18 C31 : Circle)
    (h00 : circle_with_center_through_point P26 P16 C31)
    (h01 : line_circle_intersection P03 L18 C18)
    (h02 : area_le P23 P18 P13 P08 P03 P30)
    (h03 : midpoint P26 P31 P04)
    (h04 : line_circle_intersection P19 L10 C08)
    : on_circle P16 C31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0990
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0990

theorem v06_sealed_holdout_0991
    (P02 P03 P04 P06 P07 P10 P11 P13 P15 P20 P21 P25 P28 P29 P30 : Point)
    (L14 : Line)
    (C22 : Circle)
    (h00 : tangent_chord_angle P06 P21 P29 L14 C22)
    (h01 : midpoint P04 P21 P06)
    (h02 : between P07 P02 P29)
    (h03 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    (h04 : between P13 P28 P11)
    : on_circle P29 C22 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0991
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0991

theorem v06_sealed_holdout_0992
    (P00 P02 P03 P05 P08 P11 P12 P14 P17 P18 P19 P21 P22 P26 P28 P29 P31 : Point)
    (L02 L10 L28 : Line)
    (C00 C06 : Circle)
    (h00 : tangent_chord_angle P02 P22 P28 L02 C06)
    (h01 : directed_angle_eq_mod_pi P08 P17 P26 P03 P12 P21)
    (h02 : angle_bisector_line P00 P28 P18 P29 L28)
    (h03 : directed_angle_eq_mod_pi P14 P11 P08 P05 P02 P31)
    (h04 : line_circle_intersection P19 L10 C00)
    : on_circle P28 C06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0992
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0992

theorem v06_sealed_holdout_0993
    (P01 P05 P10 P11 P15 P18 P19 P20 P21 P24 P26 P28 P29 : Point)
    (L08 L25 : Line)
    (C20 : Circle)
    (h00 : line_circle_intersection P11 L25 C20)
    (h01 : between P15 P26 P05)
    (h02 : angle_bisector_line P01 P28 P18 P29 L08)
    (h03 : midpoint P21 P20 P19)
    (h04 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    : on_line P11 L25 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0993
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0993

theorem v06_sealed_holdout_0994
    (P00 P01 P02 P03 P07 P10 P12 P14 P16 P18 P21 P22 P23 P25 P28 P29 P30 : Point)
    (L12 L29 : Line)
    (h00 : altitude P00 P01 P14 P23 L29)
    (h01 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    (h02 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h03 : between P28 P29 P30)
    (h04 : angle_bisector_line P12 P02 P18 P28 L12)
    : on_line P14 L29 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0994
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0994

theorem v06_sealed_holdout_0995
    (P03 P04 P06 P09 P19 P20 P21 P29 : Point)
    (L02 L24 : Line)
    (C02 C06 C18 C30 : Circle)
    (h00 : angle_bisector_line P21 P04 P20 P29 L24)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : between P03 P06 P09)
    (h04 : line_circle_intersection P03 L02 C30)
    : on_line P21 L24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0995
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0995

theorem v06_sealed_holdout_0996
    (P01 P02 P03 P05 P07 P08 P15 P17 P19 P29 : Point)
    (L18 L20 : Line)
    (C10 C18 : Circle)
    (h00 : angle_bisector_line P17 P05 P19 P29 L20)
    (h01 : midpoint P01 P08 P15)
    (h02 : line_circle_intersection P03 L18 C18)
    (h03 : between P07 P02 P29)
    (h04 : circle_circle_intersection P03 C10 C18)
    : on_line P17 L20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0996
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0996

theorem v06_sealed_holdout_0997
    (P02 P03 P04 P05 P06 P10 P11 P13 P17 P20 P22 P23 P24 P25 P27 P30 P31 : Point)
    (L02 : Line)
    (C14 : Circle)
    (h00 : equilateral P27 P25 P02)
    (h01 : area_le P11 P30 P17 P04 P23 P10)
    (h02 : line_circle_intersection P03 L02 C14)
    (h03 : directed_angle_eq_mod_pi P17 P24 P31 P06 P13 P20)
    (h04 : midpoint P20 P05 P22)
    : equal_length P27 P25 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0997
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0997

theorem v06_sealed_holdout_0998
    (P01 P03 P17 P19 P20 P21 P23 P25 P26 P28 P29 : Point)
    (L02 L12 L18 : Line)
    (C06 C10 : Circle)
    (h00 : equilateral P23 P26 P01)
    (h01 : angle_bisector_line P28 P25 P17 P29 L12)
    (h02 : line_circle_intersection P03 L02 C06)
    (h03 : midpoint P21 P20 P19)
    (h04 : line_circle_intersection P03 L18 C10)
    : equal_length P23 P26 P26 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0998
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0998

theorem v06_sealed_holdout_0999
    (P00 P03 P16 P19 P22 P24 P26 P27 : Point)
    (L18 L28 : Line)
    (C02 C22 : Circle)
    (h00 : equilateral P19 P27 P00)
    (h01 : angle_bisector_line P24 P26 P16 P27 L28)
    (h02 : between P22 P03 P16)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : line_circle_intersection P03 L18 C02)
    : equal_length P19 P27 P27 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_0999
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_0999

theorem v06_sealed_holdout_1000
    (P00 P03 P04 P06 P09 P12 P13 P14 P15 P16 P18 P19 P23 P24 P25 P26 P30 P31 : Point)
    (C02 C06 : Circle)
    (h00 : length_sum P24 P13 P30 P09 P16 P23)
    (h01 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    (h02 : circle_circle_intersection P19 C06 C02)
    (h03 : between P00 P25 P18)
    (h04 : directed_angle_eq_mod_pi P03 P06 P09 P12 P15 P18)
    : length_sum P30 P09 P24 P13 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1000
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1000

theorem v06_sealed_holdout_1001
    (P03 P05 P15 P16 P19 P21 P23 P27 : Point)
    (L02 : Line)
    (C02 C14 C18 C19 C22 : Circle)
    (h00 : equal_length P21 P23 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : circle_circle_intersection P03 C18 C19)
    (h03 : circle_circle_intersection P19 C14 C02)
    (h04 : line_circle_intersection P03 L02 C22)
    : equal_length P21 P23 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1001
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1001

theorem v06_sealed_holdout_1002
    (P02 P03 P10 P11 P12 P13 P17 P19 P22 P23 P24 P27 P30 : Point)
    (L02 L10 : Line)
    (C00 C14 : Circle)
    (h00 : area_eq P10 P27 P22 P02 P12 P23)
    (h01 : area_eq P02 P12 P23 P03 P13 P24)
    (h02 : midpoint P11 P30 P17)
    (h03 : line_circle_intersection P03 L02 C14)
    (h04 : line_circle_intersection P19 L10 C00)
    : area_eq P10 P27 P22 P03 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1002
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1002

theorem v06_sealed_holdout_1003
    (P04 P05 P07 P11 P15 P16 P17 P18 P19 P20 P21 P23 P24 P27 P28 : Point)
    (L00 : Line)
    (h00 : equal_length P23 P24 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : between P18 P07 P28)
    (h03 : area_le P21 P20 P19 P18 P17 P16)
    (h04 : angle_bisector_line P11 P04 P16 P27 L00)
    : equal_length P23 P24 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1003
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1003

theorem v06_sealed_holdout_1004
    (P02 P03 P07 P08 P10 P12 P13 P16 P21 P23 P25 P28 P29 P30 P31 : Point)
    (L28 : Line)
    (h00 : angle_bisector_line P13 P08 P25 P03 L28)
    (h01 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h02 : between P28 P29 P30)
    (h03 : midpoint P31 P10 P21)
    (h04 : between P02 P23 P12)
    : angle_bisector P13 P08 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1004
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1004

theorem v06_sealed_holdout_1005
    (P00 P03 P06 P07 P09 P10 P12 P13 P15 P16 P18 P19 P24 P26 P27 P30 : Point)
    (L00 L26 : Line)
    (C02 C06 : Circle)
    (h00 : angle_bisector_line P09 P10 P24 P03 L26)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : angle_bisector_line P03 P30 P16 P27 L00)
    (h03 : directed_angle_eq_mod_pi P03 P06 P09 P12 P15 P18)
    (h04 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    : angle_bisector P09 P10 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1005
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1005

theorem v06_sealed_holdout_1006
    (P02 P03 P04 P07 P09 P11 P13 P15 P16 P17 P18 P23 P24 P26 P28 P29 P31 : Point)
    (L02 : Line)
    (C22 : Circle)
    (h00 : directed_angle_eq_mod_pi P18 P16 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P17 P24)
    (h02 : midpoint P07 P02 P29)
    (h03 : line_circle_intersection P03 L02 C22)
    (h04 : directed_angle_eq_mod_pi P13 P28 P11 P26 P09 P24)
    : directed_angle_eq_mod_pi P18 P16 P04 P07 P17 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1006
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1006

theorem v06_sealed_holdout_1007
    (P02 P04 P05 P07 P08 P10 P15 P16 P19 P20 P21 P25 P27 P30 : Point)
    (L10 L16 L24 : Line)
    (C00 : Circle)
    (h00 : directed_angle_eq_mod_2pi P07 P20 P10 P21 P30 P08)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P08 P16 P25 P02)
    (h02 : angle_bisector_line P05 P30 P16 P27 L24)
    (h03 : line_circle_intersection P19 L10 C00)
    (h04 : angle_bisector_line P15 P04 P16 P27 L16)
    : directed_angle_eq_mod_2pi P07 P20 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1007
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1007

theorem v06_sealed_holdout_1008
    (P03 P04 P07 P15 P16 P17 P18 P19 P20 P21 P23 P24 P31 : Point)
    (L18 : Line)
    (C02 C10 C30 : Circle)
    (h00 : directed_angle_eq_mod_pi P20 P16 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P17 P24)
    (h02 : area_le P21 P20 P19 P18 P17 P16)
    (h03 : line_circle_intersection P03 L18 C10)
    (h04 : circle_circle_intersection P19 C30 C02)
    : directed_angle_eq_mod_pi P20 P16 P04 P07 P17 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1008
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1008

theorem v06_sealed_holdout_1009
    (P00 P01 P02 P07 P09 P10 P11 P12 P16 P20 P21 P22 P23 P25 P27 P30 P31 : Point)
    (L16 : Line)
    (h00 : directed_angle_eq_mod_2pi P09 P20 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : angle_bisector_line P07 P30 P16 P27 L16)
    (h03 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    (h04 : area_le P02 P23 P12 P01 P22 P11)
    : directed_angle_eq_mod_2pi P09 P20 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1009
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1009

theorem v06_sealed_holdout_1010
    (P00 P03 P04 P06 P07 P09 P11 P12 P13 P15 P16 P18 P19 P25 P26 P27 P29 P30 P31 : Point)
    (L20 : Line)
    (C13 : Circle)
    (h00 : circle_through_three_noncollinear_points P30 P31 P16 C13)
    (h01 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    (h02 : area_le P03 P06 P09 P12 P15 P18)
    (h03 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    (h04 : angle_bisector_line P18 P04 P16 P27 L20)
    : triangle_pred P30 P31 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1010
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1010

theorem v06_sealed_holdout_1011
    (P02 P06 P09 P13 P16 P19 P20 P27 P30 P31 : Point)
    (L08 : Line)
    (C02 C06 C14 : Circle)
    (h00 : equilateral P19 P31 P06)
    (h01 : circle_circle_intersection P19 C14 C02)
    (h02 : angle_bisector_line P09 P30 P16 P27 L08)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : directed_angle_eq_mod_pi P16 P09 P02 P27 P20 P13)
    : triangle_pred P19 P31 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1011
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1011

theorem v06_sealed_holdout_1012
    (P00 P01 P03 P05 P08 P13 P15 P16 P17 P18 P23 P24 P27 P28 P30 P31 : Point)
    (L16 L24 : Line)
    (C27 : Circle)
    (h00 : circle_through_three_noncollinear_points P00 P31 P16 C27)
    (h01 : angle_bisector_line P05 P27 P16 P28 L24)
    (h02 : midpoint P17 P24 P31)
    (h03 : angle_bisector_line P15 P01 P16 P27 L16)
    (h04 : area_le P23 P18 P13 P08 P03 P30)
    : triangle_pred P00 P31 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1012
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1012

theorem v06_sealed_holdout_1013
    (P01 P03 P06 P07 P14 P19 P20 P21 P26 P27 P31 : Point)
    (L18 : Line)
    (C10 C18 C26 : Circle)
    (h00 : equilateral P21 P31 P06)
    (h01 : midpoint P21 P20 P19)
    (h02 : line_circle_intersection P03 L18 C10)
    (h03 : directed_angle_eq_mod_pi P27 P14 P01 P20 P07 P26)
    (h04 : circle_circle_intersection P03 C26 C18)
    : triangle_pred P21 P31 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1013
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1013

theorem v06_sealed_holdout_1014
    (P00 P01 P02 P03 P04 P05 P06 P10 P12 P21 P22 P23 P28 P29 P30 P31 : Point)
    (h00 : equilateral P22 P31 P06)
    (h01 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    (h02 : between P31 P10 P21)
    (h03 : between P02 P23 P12)
    (h04 : area_le P05 P04 P03 P02 P01 P00)
    : triangle_pred P22 P31 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1014
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1014

theorem v06_sealed_holdout_1015
    (P00 P01 P03 P08 P16 P17 P18 P19 P20 P21 P27 P31 : Point)
    (L18 : Line)
    (C10 : Circle)
    (h00 : P31 = P08)
    (h01 : P27 = P19)
    (h02 : P00 = P01)
    (h03 : area_le P21 P20 P19 P18 P17 P16)
    (h04 : line_circle_intersection P03 L18 C10)
    : rotation_preserves_collinear P31 P27 P00 P08 P19 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1015
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1015

theorem v06_sealed_holdout_1016
    (P00 P07 P08 P16 P19 P25 P27 P28 P29 P30 P31 : Point)
    (h00 : P27 = P08)
    (h01 : P28 = P19)
    (h02 : P31 = P00)
    (h03 : midpoint P25 P16 P07)
    (h04 : between P28 P29 P30)
    : rotation_preserves_collinear P27 P28 P31 P08 P19 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1016
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1016

theorem v06_sealed_holdout_1017
    (P03 P08 P19 P23 P29 P30 P31 : Point)
    (C02 C06 C18 : Circle)
    (h00 : P23 = P08)
    (h01 : P29 = P19)
    (h02 : P30 = P31)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : circle_circle_intersection P03 C02 C18)
    : rotation_preserves_collinear P23 P29 P30 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1017
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1017

theorem v06_sealed_holdout_1018
    (P01 P03 P04 P08 P15 P19 P20 P22 P29 P30 P31 : Point)
    (L18 : Line)
    (C18 : Circle)
    (h00 : P19 = P08)
    (h01 : P30 = P20)
    (h02 : P29 = P31)
    (h03 : directed_angle_eq_mod_pi P01 P08 P15 P22 P29 P04)
    (h04 : line_circle_intersection P03 L18 C18)
    : rotation_preserves_collinear P19 P30 P29 P08 P20 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1018
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1018

theorem v06_sealed_holdout_1019
    (P00 P03 P04 P05 P08 P12 P15 P17 P19 P21 P26 P28 P31 : Point)
    (h00 : P15 = P08)
    (h01 : P31 = P19)
    (h02 : P28 = P00)
    (h03 : between P05 P04 P03)
    (h04 : area_le P08 P17 P26 P03 P12 P21)
    : rotation_preserves_collinear P15 P31 P28 P08 P19 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1019
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1019

theorem v06_sealed_holdout_1020
    (P00 P05 P06 P09 P12 P13 P14 P15 P16 P17 P19 P23 P24 P28 : Point)
    (C02 C03 C14 : Circle)
    (h00 : circle_with_center_through_point P24 P17 C03)
    (h01 : between P06 P19 P00)
    (h02 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h03 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h04 : circle_circle_intersection P19 C14 C02)
    : on_circle P17 C03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1020
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1020

theorem v06_sealed_holdout_1021
    (P00 P01 P03 P04 P16 P19 P22 P28 P29 P30 P31 : Point)
    (L26 : Line)
    (C02 C14 C22 C26 : Circle)
    (h00 : tangent_chord_angle P04 P22 P29 L26 C26)
    (h01 : midpoint P22 P03 P16)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : area_le P28 P29 P30 P31 P00 P01)
    (h04 : circle_circle_intersection P19 C14 C02)
    : on_circle P29 C26 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1021
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1021

theorem v06_sealed_holdout_1022
    (P00 P03 P04 P12 P19 P22 P26 P27 P28 P29 P31 : Point)
    (L14 L26 : Line)
    (C02 C10 C12 C18 : Circle)
    (h00 : tangent_chord_angle P00 P22 P28 L14 C10)
    (h01 : midpoint P26 P31 P04)
    (h02 : between P29 P12 P27)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : line_circle_intersection P19 L26 C12)
    : on_circle P28 C10 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1022
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1022

theorem v06_sealed_holdout_1023
    (P01 P02 P03 P07 P08 P09 P14 P15 P19 P24 P29 : Point)
    (L18 L27 : Line)
    (C04 C10 C18 : Circle)
    (h00 : line_circle_intersection P09 L27 C04)
    (h01 : between P01 P08 P15)
    (h02 : line_circle_intersection P03 L18 C18)
    (h03 : directed_angle_eq_mod_pi P07 P02 P29 P24 P19 P14)
    (h04 : circle_circle_intersection P03 C10 C18)
    : on_line P09 L27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1023
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1023

theorem v06_sealed_holdout_1024
    (P01 P02 P03 P05 P08 P11 P14 P17 P19 P23 P30 P31 : Point)
    (L03 L10 : Line)
    (C00 C02 C18 : Circle)
    (h00 : altitude P30 P01 P14 P23 L03)
    (h01 : circle_circle_intersection P03 C02 C18)
    (h02 : between P11 P30 P17)
    (h03 : area_le P14 P11 P08 P05 P02 P31)
    (h04 : line_circle_intersection P19 L10 C00)
    : on_line P14 L03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1024
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1024

theorem v06_sealed_holdout_1025
    (P01 P03 P05 P10 P19 P20 P21 P24 P28 P29 : Point)
    (L02 L28 : Line)
    (C02 C06 C14 : Circle)
    (h00 : angle_bisector_line P19 P05 P20 P29 L28)
    (h01 : circle_circle_intersection P19 C14 C02)
    (h02 : line_circle_intersection P03 L02 C06)
    (h03 : between P21 P20 P19)
    (h04 : area_le P24 P01 P10 P19 P28 P05)
    : on_line P19 L28 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1025
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1025

theorem v06_sealed_holdout_1026
    (P01 P02 P03 P06 P15 P17 P19 P24 P26 P28 P29 : Point)
    (L02 L20 L24 L28 : Line)
    (C18 C19 C30 : Circle)
    (h00 : angle_bisector_line P15 P06 P19 P29 L24)
    (h01 : angle_bisector_line P24 P26 P17 P28 L28)
    (h02 : line_circle_intersection P03 L02 C30)
    (h03 : angle_bisector_line P02 P01 P17 P28 L20)
    (h04 : circle_circle_intersection P03 C18 C19)
    : on_line P15 L24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1026
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1026

theorem v06_sealed_holdout_1027
    (P00 P02 P03 P06 P09 P18 P25 P26 P28 P30 : Point)
    (L02 L04 : Line)
    (C30 : Circle)
    (h00 : equilateral P25 P26 P02)
    (h01 : angle_bisector_line P30 P26 P18 P28 L04)
    (h02 : between P00 P25 P18)
    (h03 : midpoint P03 P06 P09)
    (h04 : line_circle_intersection P03 L02 C30)
    : equal_length P25 P26 P26 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1027
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1027

theorem v06_sealed_holdout_1028
    (P01 P02 P03 P04 P06 P07 P08 P10 P15 P19 P20 P21 P23 P25 P27 P29 P30 : Point)
    (C02 C22 : Circle)
    (h00 : equilateral P21 P27 P01)
    (h01 : circle_circle_intersection P19 C22 C02)
    (h02 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    (h03 : between P07 P02 P29)
    (h04 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    : equal_length P21 P27 P27 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1028
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1028

theorem v06_sealed_holdout_1029
    (P00 P01 P02 P03 P04 P05 P16 P17 P19 P27 P28 P30 : Point)
    (L00 : Line)
    (C02 C18 C26 C30 : Circle)
    (h00 : equilateral P17 P28 P00)
    (h01 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    (h02 : angle_bisector_line P27 P30 P16 P28 L00)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : circle_circle_intersection P03 C26 C18)
    : equal_length P17 P28 P28 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1029
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1029

theorem v06_sealed_holdout_1030
    (P03 P05 P06 P09 P14 P15 P16 P19 P20 P21 P22 P23 P26 P27 P30 : Point)
    (C10 C18 C19 : Circle)
    (h00 : length_sum P22 P14 P30 P09 P16 P23)
    (h01 : circle_circle_intersection P03 C18 C19)
    (h02 : area_le P15 P26 P05 P16 P27 P06)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : between P21 P20 P19)
    : length_sum P30 P09 P22 P14 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1030
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1030

theorem v06_sealed_holdout_1031
    (P02 P03 P05 P10 P15 P16 P19 P22 P23 P24 P27 P28 P29 P30 : Point)
    (L20 : Line)
    (h00 : equal_length P19 P24 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : area_le P22 P03 P16 P29 P10 P23)
    (h03 : angle_bisector_line P02 P03 P16 P27 L20)
    (h04 : midpoint P28 P29 P30)
    : equal_length P19 P24 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1031
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1031

theorem v06_sealed_holdout_1032
    (P02 P03 P06 P08 P09 P12 P13 P16 P22 P23 P24 P27 P28 P30 P31 : Point)
    (L04 L18 : Line)
    (C26 : Circle)
    (h00 : area_eq P08 P28 P22 P02 P12 P23)
    (h01 : area_eq P02 P12 P23 P03 P13 P24)
    (h02 : angle_bisector_line P30 P31 P16 P27 L04)
    (h03 : line_circle_intersection P03 L18 C26)
    (h04 : midpoint P03 P06 P09)
    : area_eq P08 P28 P22 P03 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1032
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1032

theorem v06_sealed_holdout_1033
    (P03 P05 P15 P16 P19 P21 P24 P27 : Point)
    (L18 L26 : Line)
    (C04 C10 C18 : Circle)
    (h00 : equal_length P21 P24 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : line_circle_intersection P03 L18 C18)
    (h03 : line_circle_intersection P19 L26 C04)
    (h04 : circle_circle_intersection P03 C10 C18)
    : equal_length P21 P24 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1033
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1033

theorem v06_sealed_holdout_1034
    (P01 P03 P04 P08 P09 P10 P11 P14 P17 P23 P25 P28 P30 : Point)
    (L20 L30 : Line)
    (C18 C19 : Circle)
    (h00 : angle_bisector_line P11 P09 P25 P03 L30)
    (h01 : area_le P11 P30 P17 P04 P23 P10)
    (h02 : midpoint P14 P11 P08)
    (h03 : angle_bisector_line P10 P01 P17 P28 L20)
    (h04 : circle_circle_intersection P03 C18 C19)
    : angle_bisector P11 P09 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1034
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1034

theorem v06_sealed_holdout_1035
    (P03 P05 P06 P07 P10 P15 P16 P18 P19 P20 P21 P24 P26 P27 P28 : Point)
    (L28 : Line)
    (C02 C18 : Circle)
    (h00 : angle_bisector_line P07 P10 P24 P03 L28)
    (h01 : area_le P15 P26 P05 P16 P27 P06)
    (h02 : between P18 P07 P28)
    (h03 : midpoint P21 P20 P19)
    (h04 : circle_circle_intersection P03 C02 C18)
    : angle_bisector P07 P10 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1035
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1035

theorem v06_sealed_holdout_1036
    (P00 P04 P07 P10 P11 P15 P16 P17 P18 P21 P22 P23 P24 P25 P28 P29 P30 P31 : Point)
    (h00 : directed_angle_eq_mod_pi P16 P17 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P18 P24)
    (h02 : midpoint P25 P16 P07)
    (h03 : midpoint P28 P29 P30)
    (h04 : area_le P31 P10 P21 P00 P11 P22)
    : directed_angle_eq_mod_pi P16 P17 P04 P07 P18 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1036
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1036

theorem v06_sealed_holdout_1037
    (P00 P02 P03 P04 P05 P07 P08 P10 P11 P16 P18 P21 P22 P25 P27 P29 P30 : Point)
    (L02 L28 : Line)
    (C30 : Circle)
    (h00 : directed_angle_eq_mod_2pi P05 P21 P10 P22 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P22 P30 P07 P16 P25 P02)
    (h02 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    (h03 : angle_bisector_line P08 P02 P16 P27 L28)
    (h04 : line_circle_intersection P03 L02 C30)
    : directed_angle_eq_mod_2pi P05 P21 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1037
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1037

theorem v06_sealed_holdout_1038
    (P02 P03 P04 P07 P09 P10 P11 P13 P15 P16 P17 P18 P20 P23 P24 P25 P26 P28 P29 P30 P31 : Point)
    (h00 : directed_angle_eq_mod_pi P18 P17 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : midpoint P07 P02 P29)
    (h03 : area_le P10 P15 P20 P25 P30 P03)
    (h04 : area_le P13 P28 P11 P26 P09 P24)
    : directed_angle_eq_mod_pi P18 P17 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1038
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1038

theorem v06_sealed_holdout_1039
    (P02 P05 P07 P08 P10 P16 P17 P20 P21 P22 P24 P25 P27 P30 P31 : Point)
    (L24 : Line)
    (h00 : directed_angle_eq_mod_2pi P07 P21 P10 P22 P30 P08)
    (h01 : directed_angle_eq_mod_2pi P22 P30 P08 P16 P25 P02)
    (h02 : angle_bisector_line P05 P31 P16 P27 L24)
    (h03 : between P17 P24 P31)
    (h04 : midpoint P20 P05 P22)
    : directed_angle_eq_mod_2pi P07 P21 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1039
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1039

theorem v06_sealed_holdout_1040
    (P00 P01 P02 P03 P11 P14 P16 P19 P27 P28 : Point)
    (L00 L02 L10 : Line)
    (C06 C24 C31 : Circle)
    (h00 : circle_through_three_noncollinear_points P28 P00 P16 C31)
    (h01 : line_circle_intersection P03 L02 C06)
    (h02 : line_circle_intersection P19 L10 C24)
    (h03 : angle_bisector_line P11 P02 P16 P27 L00)
    (h04 : between P27 P14 P01)
    : triangle_pred P28 P00 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1040
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1040

theorem v06_sealed_holdout_1041
    (P00 P02 P03 P06 P10 P11 P12 P17 P19 P21 P22 P23 P31 : Point)
    (L18 : Line)
    (C02 C22 : Circle)
    (h00 : equilateral P17 P00 P06)
    (h01 : circle_circle_intersection P19 C22 C02)
    (h02 : line_circle_intersection P03 L18 C02)
    (h03 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    (h04 : between P02 P23 P12)
    : triangle_pred P17 P00 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1041
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1041

theorem v06_sealed_holdout_1042
    (P00 P03 P04 P06 P09 P11 P16 P18 P19 P25 P29 P30 : Point)
    (C02 C13 C18 C22 C26 : Circle)
    (h00 : circle_through_three_noncollinear_points P30 P00 P16 C13)
    (h01 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    (h02 : midpoint P03 P06 P09)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : circle_circle_intersection P19 C22 C02)
    : triangle_pred P30 P00 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1042
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1042

theorem v06_sealed_holdout_1043
    (P00 P03 P06 P09 P11 P13 P19 P24 P26 P28 : Point)
    (L02 L18 L26 : Line)
    (C04 C22 C26 : Circle)
    (h00 : equilateral P19 P00 P06)
    (h01 : line_circle_intersection P19 L26 C04)
    (h02 : line_circle_intersection P03 L02 C22)
    (h03 : directed_angle_eq_mod_pi P13 P28 P11 P26 P09 P24)
    (h04 : line_circle_intersection P03 L18 C26)
    : triangle_pred P19 P00 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1043
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1043

theorem v06_sealed_holdout_1044
    (P00 P03 P05 P06 P07 P08 P09 P11 P13 P14 P18 P19 P20 P22 P23 P24 P30 : Point)
    (L10 : Line)
    (C00 : Circle)
    (h00 : equilateral P20 P00 P06)
    (h01 : midpoint P14 P11 P08)
    (h02 : line_circle_intersection P19 L10 C00)
    (h03 : directed_angle_eq_mod_pi P20 P05 P22 P07 P24 P09)
    (h04 : area_le P23 P18 P13 P08 P03 P30)
    : triangle_pred P20 P00 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1044
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1044

theorem v06_sealed_holdout_1045
    (P00 P02 P07 P08 P10 P14 P15 P19 P20 P24 P28 P29 P31 : Point)
    (h00 : P29 = P08)
    (h01 : P28 = P19)
    (h02 : P00 = P31)
    (h03 : directed_angle_eq_mod_pi P07 P02 P29 P24 P19 P14)
    (h04 : midpoint P10 P15 P20)
    : rotation_preserves_collinear P29 P28 P00 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1045
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1045

theorem v06_sealed_holdout_1046
    (P00 P02 P05 P08 P11 P14 P19 P25 P29 P31 : Point)
    (C02 C30 : Circle)
    (h00 : P25 = P08)
    (h01 : P29 = P19)
    (h02 : P31 = P00)
    (h03 : circle_circle_intersection P19 C30 C02)
    (h04 : area_le P14 P11 P08 P05 P02 P31)
    : rotation_preserves_collinear P25 P29 P31 P08 P19 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1046
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1046

theorem v06_sealed_holdout_1047
    (P00 P05 P06 P07 P08 P15 P16 P17 P18 P19 P21 P26 P27 P28 P30 P31 : Point)
    (h00 : P21 = P08)
    (h01 : P30 = P19)
    (h02 : P31 = P00)
    (h03 : area_le P15 P26 P05 P16 P27 P06)
    (h04 : area_le P18 P07 P28 P17 P06 P27)
    : rotation_preserves_collinear P21 P30 P31 P08 P19 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1047
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1047

theorem v06_sealed_holdout_1048
    (P00 P01 P03 P08 P10 P16 P17 P19 P22 P23 P24 P28 P29 P31 : Point)
    (L28 : Line)
    (h00 : P17 = P08)
    (h01 : P31 = P19)
    (h02 : P29 = P00)
    (h03 : angle_bisector_line P24 P01 P17 P28 L28)
    (h04 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    : rotation_preserves_collinear P17 P31 P29 P08 P19 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1048
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1048

theorem v06_sealed_holdout_1049
    (P00 P03 P08 P13 P18 P19 P23 P28 P30 P31 : Point)
    (L02 : Line)
    (C22 : Circle)
    (h00 : P13 = P08)
    (h01 : P00 = P19)
    (h02 : P28 = P31)
    (h03 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    (h04 : line_circle_intersection P03 L02 C22)
    : rotation_preserves_collinear P13 P00 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1049
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1049

theorem v06_sealed_holdout_1050
    (P11 P16 P17 P18 P19 P22 P24 P27 P28 P30 P31 : Point)
    (L00 L10 L28 : Line)
    (C00 C07 : Circle)
    (h00 : circle_with_center_through_point P22 P18 C07)
    (h01 : angle_bisector_line P11 P28 P16 P27 L00)
    (h02 : angle_bisector_line P16 P31 P17 P27 L28)
    (h03 : between P30 P27 P24)
    (h04 : line_circle_intersection P19 L10 C00)
    : on_circle P18 C07 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1050
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1050

theorem v06_sealed_holdout_1051
    (P02 P03 P08 P11 P12 P17 P19 P21 P23 P26 P29 P30 : Point)
    (L02 L06 : Line)
    (C02 C14 C22 C30 : Circle)
    (h00 : tangent_chord_angle P02 P23 P29 L06 C30)
    (h01 : directed_angle_eq_mod_pi P08 P17 P26 P03 P12 P21)
    (h02 : between P11 P30 P17)
    (h03 : line_circle_intersection P03 L02 C14)
    (h04 : circle_circle_intersection P19 C22 C02)
    : on_circle P29 C30 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1051
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1051

theorem v06_sealed_holdout_1052
    (P07 P12 P13 P14 P18 P19 P20 P21 P23 P28 P30 : Point)
    (L26 : Line)
    (C02 C14 : Circle)
    (h00 : tangent_chord_angle P30 P23 P28 L26 C14)
    (h01 : between P12 P13 P14)
    (h02 : circle_circle_intersection P19 C14 C02)
    (h03 : midpoint P18 P07 P28)
    (h04 : midpoint P21 P20 P19)
    : on_circle P28 C14 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1052
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1052

theorem v06_sealed_holdout_1053
    (P03 P07 P16 P19 P22 P25 : Point)
    (L10 L18 L29 : Line)
    (C02 C16 C20 : Circle)
    (h00 : line_circle_intersection P07 L29 C20)
    (h01 : between P19 P22 P25)
    (h02 : midpoint P22 P03 P16)
    (h03 : line_circle_intersection P19 L10 C16)
    (h04 : line_circle_intersection P03 L18 C02)
    : on_line P07 L29 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1053
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1053

theorem v06_sealed_holdout_1054
    (P00 P02 P04 P08 P09 P10 P12 P14 P18 P19 P23 P25 P26 P27 P28 P29 P31 : Point)
    (L09 L28 : Line)
    (h00 : altitude P28 P02 P14 P23 L09)
    (h01 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    (h02 : directed_angle_eq_mod_pi P29 P12 P27 P10 P25 P08)
    (h03 : midpoint P00 P25 P18)
    (h04 : angle_bisector_line P08 P04 P18 P28 L28)
    : on_line P14 L09 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1054
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1054

theorem v06_sealed_holdout_1055
    (P03 P06 P10 P15 P17 P18 P19 P20 P26 P27 P28 P29 : Point)
    (L00 L18 L20 L26 : Line)
    (C04 C18 : Circle)
    (h00 : angle_bisector_line P17 P06 P20 P29 L00)
    (h01 : angle_bisector_line P26 P27 P18 P28 L20)
    (h02 : line_circle_intersection P03 L18 C18)
    (h03 : line_circle_intersection P19 L26 C04)
    (h04 : midpoint P10 P15 P20)
    : on_line P17 L00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1055
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1055

theorem v06_sealed_holdout_1056
    (P03 P06 P08 P12 P13 P17 P19 P21 P26 P29 : Point)
    (L26 L28 : Line)
    (C02 C06 C18 C26 C28 : Circle)
    (h00 : angle_bisector_line P13 P06 P19 P29 L28)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : directed_angle_eq_mod_pi P08 P17 P26 P03 P12 P21)
    (h03 : line_circle_intersection P19 L26 C28)
    (h04 : circle_circle_intersection P03 C26 C18)
    : on_line P13 L28 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1056
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1056

theorem v06_sealed_holdout_1057
    (P01 P02 P04 P11 P16 P17 P18 P19 P20 P21 P23 P27 P28 P30 : Point)
    (L00 L08 : Line)
    (C02 C14 : Circle)
    (h00 : equilateral P23 P27 P02)
    (h01 : circle_circle_intersection P19 C14 C02)
    (h02 : angle_bisector_line P01 P30 P18 P28 L08)
    (h03 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    (h04 : angle_bisector_line P11 P04 P18 P28 L00)
    : equal_length P23 P27 P27 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1057
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1057

theorem v06_sealed_holdout_1058
    (P00 P01 P03 P16 P19 P22 P28 P29 P30 P31 : Point)
    (C02 C22 C30 : Circle)
    (h00 : equilateral P19 P28 P01)
    (h01 : circle_circle_intersection P19 C30 C02)
    (h02 : between P22 P03 P16)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : directed_angle_eq_mod_pi P28 P29 P30 P31 P00 P01)
    : equal_length P19 P28 P28 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1058
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1058

theorem v06_sealed_holdout_1059
    (P00 P03 P04 P13 P15 P18 P19 P23 P26 P29 P31 : Point)
    (L18 : Line)
    (C02 C06 C26 : Circle)
    (h00 : equilateral P15 P29 P00)
    (h01 : between P23 P18 P13)
    (h02 : midpoint P26 P31 P04)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : line_circle_intersection P03 L18 C26)
    : equal_length P15 P29 P29 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1059
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1059

theorem v06_sealed_holdout_1060
    (P02 P04 P06 P07 P08 P09 P15 P16 P20 P21 P23 P24 P25 P26 P27 P29 P30 P31 : Point)
    (L20 : Line)
    (h00 : length_sum P20 P15 P30 P09 P16 P23)
    (h01 : midpoint P30 P27 P24)
    (h02 : angle_bisector_line P26 P31 P16 P27 L20)
    (h03 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    (h04 : between P07 P02 P29)
    : length_sum P30 P09 P20 P15 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1060
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1060

theorem v06_sealed_holdout_1061
    (P03 P04 P05 P08 P10 P11 P12 P14 P15 P16 P17 P21 P23 P25 P26 P27 P30 : Point)
    (h00 : equal_length P17 P25 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : area_le P08 P17 P26 P03 P12 P21)
    (h03 : area_le P11 P30 P17 P04 P23 P10)
    (h04 : between P14 P11 P08)
    : equal_length P17 P25 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1061
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1061

theorem v06_sealed_holdout_1062
    (P02 P03 P06 P12 P13 P19 P22 P23 P24 P29 : Point)
    (L10 L26 : Line)
    (C10 C18 C20 C24 : Circle)
    (h00 : area_eq P06 P29 P22 P02 P12 P23)
    (h01 : area_eq P02 P12 P23 P03 P13 P24)
    (h02 : line_circle_intersection P19 L26 C20)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : line_circle_intersection P19 L10 C24)
    : area_eq P06 P29 P22 P03 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1062
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1062

theorem v06_sealed_holdout_1063
    (P03 P05 P15 P16 P19 P22 P25 P27 : Point)
    (L10 L18 : Line)
    (C02 C16 : Circle)
    (h00 : equal_length P19 P25 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : midpoint P22 P03 P16)
    (h03 : line_circle_intersection P19 L10 C16)
    (h04 : line_circle_intersection P03 L18 C02)
    : equal_length P19 P25 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1063
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1063

theorem v06_sealed_holdout_1064
    (P00 P03 P04 P06 P09 P10 P11 P17 P18 P19 P25 P28 P29 P30 : Point)
    (L00 L04 : Line)
    (h00 : angle_bisector_line P09 P10 P25 P03 L00)
    (h01 : angle_bisector_line P30 P28 P17 P29 L04)
    (h02 : area_le P00 P25 P18 P11 P04 P29)
    (h03 : midpoint P03 P06 P09)
    (h04 : between P06 P19 P00)
    : angle_bisector P09 P10 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1064
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1064

theorem v06_sealed_holdout_1065
    (P01 P02 P03 P04 P05 P06 P07 P08 P11 P14 P15 P19 P21 P22 P23 P24 P25 P29 : Point)
    (L30 : Line)
    (C10 C18 : Circle)
    (h00 : angle_bisector_line P05 P11 P24 P03 L30)
    (h01 : directed_angle_eq_mod_pi P01 P08 P15 P22 P29 P04)
    (h02 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    (h03 : directed_angle_eq_mod_pi P07 P02 P29 P24 P19 P14)
    (h04 : circle_circle_intersection P03 C10 C18)
    : angle_bisector P05 P11 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1065
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1065

theorem v06_sealed_holdout_1066
    (P03 P04 P06 P07 P13 P14 P15 P16 P17 P18 P19 P20 P23 P24 P31 : Point)
    (L26 : Line)
    (C18 C26 C28 : Circle)
    (h00 : directed_angle_eq_mod_pi P14 P18 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : line_circle_intersection P19 L26 C28)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : area_le P17 P24 P31 P06 P13 P20)
    : directed_angle_eq_mod_pi P14 P18 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1066
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1066

theorem v06_sealed_holdout_1067
    (P01 P02 P03 P06 P07 P10 P16 P17 P18 P19 P20 P21 P22 P24 P25 P27 P28 P30 : Point)
    (h00 : directed_angle_eq_mod_2pi P03 P22 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : area_le P18 P07 P28 P17 P06 P27)
    (h03 : midpoint P21 P20 P19)
    (h04 : midpoint P24 P01 P10)
    : directed_angle_eq_mod_2pi P03 P22 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1067
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1067

theorem v06_sealed_holdout_1068
    (P00 P01 P04 P07 P15 P16 P17 P18 P19 P23 P24 P25 P28 P29 P30 P31 : Point)
    (L26 : Line)
    (C20 : Circle)
    (h00 : directed_angle_eq_mod_pi P16 P18 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P17 P24)
    (h02 : between P25 P16 P07)
    (h03 : area_le P28 P29 P30 P31 P00 P01)
    (h04 : line_circle_intersection P19 L26 C20)
    : directed_angle_eq_mod_pi P16 P18 P04 P07 P17 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1068
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1068

theorem v06_sealed_holdout_1069
    (P00 P02 P03 P05 P06 P07 P09 P10 P13 P16 P18 P19 P21 P22 P25 P26 P30 : Point)
    (h00 : directed_angle_eq_mod_2pi P05 P22 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : between P00 P25 P18)
    (h03 : between P03 P06 P09)
    (h04 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    : directed_angle_eq_mod_2pi P05 P22 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1069
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1069

theorem v06_sealed_holdout_1070
    (P01 P03 P16 P19 P26 P27 P29 P31 : Point)
    (L10 L16 L26 : Line)
    (C04 C08 C10 C17 C18 : Circle)
    (h00 : circle_through_three_noncollinear_points P26 P01 P16 C17)
    (h01 : angle_bisector_line P31 P29 P16 P27 L16)
    (h02 : line_circle_intersection P19 L26 C04)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : line_circle_intersection P19 L10 C08)
    : triangle_pred P26 P01 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1070
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1070

theorem v06_sealed_holdout_1071
    (P01 P02 P03 P04 P05 P06 P08 P10 P11 P13 P14 P15 P17 P20 P23 P24 P30 P31 : Point)
    (L18 : Line)
    (C18 : Circle)
    (h00 : equilateral P15 P01 P06)
    (h01 : area_le P11 P30 P17 P04 P23 P10)
    (h02 : area_le P14 P11 P08 P05 P02 P31)
    (h03 : area_le P17 P24 P31 P06 P13 P20)
    (h04 : line_circle_intersection P03 L18 C18)
    : triangle_pred P15 P01 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1071
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1071

theorem v06_sealed_holdout_1072
    (P01 P05 P06 P07 P10 P16 P17 P18 P19 P20 P21 P24 P27 P28 : Point)
    (L28 : Line)
    (C31 : Circle)
    (h00 : circle_through_three_noncollinear_points P28 P01 P16 C31)
    (h01 : area_le P18 P07 P28 P17 P06 P27)
    (h02 : directed_angle_eq_mod_pi P21 P20 P19 P18 P17 P16)
    (h03 : directed_angle_eq_mod_pi P24 P01 P10 P19 P28 P05)
    (h04 : angle_bisector_line P16 P06 P17 P27 L28)
    : triangle_pred P28 P01 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1072
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1072

theorem v06_sealed_holdout_1073
    (P00 P01 P02 P06 P07 P10 P11 P12 P16 P17 P21 P22 P23 P25 P28 P29 P30 P31 : Point)
    (h00 : equilateral P17 P01 P06)
    (h01 : midpoint P25 P16 P07)
    (h02 : area_le P28 P29 P30 P31 P00 P01)
    (h03 : directed_angle_eq_mod_pi P31 P10 P21 P00 P11 P22)
    (h04 : directed_angle_eq_mod_pi P02 P23 P12 P01 P22 P11)
    : triangle_pred P17 P01 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1073
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1073

theorem v06_sealed_holdout_1074
    (P00 P01 P03 P06 P09 P13 P16 P18 P23 P27 P29 : Point)
    (L00 L24 : Line)
    (h00 : equilateral P18 P01 P06)
    (h01 : angle_bisector_line P03 P29 P16 P27 L00)
    (h02 : between P03 P06 P09)
    (h03 : angle_bisector_line P13 P03 P16 P27 L24)
    (h04 : midpoint P09 P00 P23)
    : triangle_pred P18 P01 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1074
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1074

theorem v06_sealed_holdout_1075
    (P00 P02 P08 P19 P20 P27 P28 P29 P30 P31 : Point)
    (L20 : Line)
    (h00 : P27 = P08)
    (h01 : P29 = P19)
    (h02 : P00 = P31)
    (h03 : angle_bisector_line P02 P00 P20 P28 L20)
    (h04 : midpoint P28 P29 P30)
    : rotation_preserves_collinear P27 P29 P00 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1075
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1075

theorem v06_sealed_holdout_1076
    (P00 P01 P08 P18 P19 P23 P25 P28 P30 P31 : Point)
    (L04 : Line)
    (h00 : P23 = P08)
    (h01 : P30 = P19)
    (h02 : P31 = P00)
    (h03 : angle_bisector_line P30 P01 P19 P28 L04)
    (h04 : between P00 P25 P18)
    : rotation_preserves_collinear P23 P30 P31 P08 P19 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1076
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1076

theorem v06_sealed_holdout_1077
    (P00 P01 P04 P06 P08 P15 P19 P20 P21 P30 P31 : Point)
    (h00 : P19 = P08)
    (h01 : P31 = P20)
    (h02 : P30 = P00)
    (h03 : midpoint P01 P08 P15)
    (h04 : between P04 P21 P06)
    : rotation_preserves_collinear P19 P31 P30 P08 P20 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1077
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1077

theorem v06_sealed_holdout_1078
    (P00 P01 P02 P03 P04 P05 P08 P12 P15 P17 P19 P21 P26 P29 P31 : Point)
    (h00 : P15 = P08)
    (h01 : P00 = P19)
    (h02 : P29 = P31)
    (h03 : area_le P05 P04 P03 P02 P01 P00)
    (h04 : area_le P08 P17 P26 P03 P12 P21)
    : rotation_preserves_collinear P15 P00 P29 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1078
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1078

theorem v06_sealed_holdout_1079
    (P00 P01 P03 P05 P08 P09 P11 P14 P19 P23 P28 P31 : Point)
    (L18 : Line)
    (C02 : Circle)
    (h00 : P11 = P08)
    (h01 : P01 = P19)
    (h02 : P28 = P31)
    (h03 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h04 : line_circle_intersection P03 L18 C02)
    : rotation_preserves_collinear P11 P01 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1079
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1079

theorem v06_sealed_holdout_1080
    (P03 P10 P11 P13 P15 P19 P20 P28 : Point)
    (L26 : Line)
    (C02 C11 C12 C18 : Circle)
    (h00 : circle_with_center_through_point P20 P19 C11)
    (h01 : midpoint P10 P15 P20)
    (h02 : midpoint P13 P28 P11)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : line_circle_intersection P19 L26 C12)
    : on_circle P19 C11 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1080
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1080

theorem v06_sealed_holdout_1081
    (P00 P04 P11 P18 P19 P23 P25 P26 P28 P29 P30 P31 : Point)
    (L04 L18 L26 : Line)
    (C02 C12 : Circle)
    (h00 : tangent_chord_angle P00 P23 P29 L18 C02)
    (h01 : midpoint P26 P31 P04)
    (h02 : angle_bisector_line P30 P31 P19 P28 L04)
    (h03 : area_le P00 P25 P18 P11 P04 P29)
    (h04 : line_circle_intersection P19 L26 C12)
    : on_circle P29 C02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1081
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1081

theorem v06_sealed_holdout_1082
    (P03 P04 P06 P09 P10 P15 P19 P20 P21 P25 P30 : Point)
    (L01 L10 : Line)
    (C00 C02 C04 C14 : Circle)
    (h00 : line_circle_intersection P09 L01 C04)
    (h01 : line_circle_intersection P19 L10 C00)
    (h02 : midpoint P04 P21 P06)
    (h03 : circle_circle_intersection P19 C14 C02)
    (h04 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    : on_line P09 L01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1082
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1082

theorem v06_sealed_holdout_1083
    (P00 P01 P02 P03 P04 P05 P08 P11 P12 P14 P17 P18 P21 P26 P28 : Point)
    (L28 L31 : Line)
    (C04 : Circle)
    (h00 : line_circle_intersection P05 L31 C04)
    (h01 : area_le P05 P04 P03 P02 P01 P00)
    (h02 : directed_angle_eq_mod_pi P08 P17 P26 P03 P12 P21)
    (h03 : angle_bisector_line P00 P02 P18 P28 L28)
    (h04 : midpoint P14 P11 P08)
    : on_line P05 L31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1083
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1083

theorem v06_sealed_holdout_1084
    (P01 P05 P06 P10 P15 P16 P19 P20 P21 P24 P26 P27 P28 P29 P30 : Point)
    (L08 : Line)
    (h00 : angle_bisector_line P19 P06 P21 P29 L08)
    (h01 : area_le P15 P26 P05 P16 P27 P06)
    (h02 : angle_bisector_line P01 P30 P19 P28 L08)
    (h03 : between P21 P20 P19)
    (h04 : between P24 P01 P10)
    : on_line P19 L08 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1084
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1084

theorem v06_sealed_holdout_1085
    (P03 P07 P10 P15 P16 P19 P20 P22 P23 P25 P29 : Point)
    (L04 L18 L26 : Line)
    (C02 C12 : Circle)
    (h00 : angle_bisector_line P15 P07 P20 P29 L04)
    (h01 : line_circle_intersection P19 L26 C12)
    (h02 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    (h03 : midpoint P25 P16 P07)
    (h04 : line_circle_intersection P03 L18 C02)
    : on_line P15 L04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1085
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1085

theorem v06_sealed_holdout_1086
    (P03 P04 P07 P11 P19 P26 P29 P31 : Point)
    (L00 L26 : Line)
    (C02 C04 C06 C18 : Circle)
    (h00 : angle_bisector_line P11 P07 P19 P29 L00)
    (h01 : line_circle_intersection P19 L26 C04)
    (h02 : midpoint P26 P31 P04)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : circle_circle_intersection P03 C02 C18)
    : on_line P11 L00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1086
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1086

theorem v06_sealed_holdout_1087
    (P00 P01 P02 P03 P04 P07 P08 P10 P15 P18 P20 P21 P22 P25 P28 P29 P30 P31 : Point)
    (L16 : Line)
    (h00 : equilateral P21 P28 P02)
    (h01 : area_le P01 P08 P15 P22 P29 P04)
    (h02 : angle_bisector_line P31 P00 P18 P28 L16)
    (h03 : midpoint P07 P02 P29)
    (h04 : area_le P10 P15 P20 P25 P30 P03)
    : equal_length P21 P28 P28 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1087
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1087

theorem v06_sealed_holdout_1088
    (P01 P08 P11 P14 P17 P19 P26 P29 P30 : Point)
    (C02 C06 : Circle)
    (h00 : equilateral P17 P29 P01)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : between P08 P17 P26)
    (h03 : between P11 P30 P17)
    (h04 : midpoint P14 P11 P08)
    : equal_length P17 P29 P29 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1088
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1088

theorem v06_sealed_holdout_1089
    (P00 P03 P05 P09 P12 P13 P14 P15 P16 P17 P23 P26 P30 : Point)
    (C10 C18 : Circle)
    (h00 : equilateral P13 P30 P00)
    (h01 : between P09 P00 P23)
    (h02 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h03 : midpoint P15 P26 P05)
    (h04 : circle_circle_intersection P03 C10 C18)
    : equal_length P13 P30 P30 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1089
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1089

theorem v06_sealed_holdout_1090
    (P03 P09 P10 P15 P16 P18 P19 P22 P23 P25 P27 P29 P30 : Point)
    (L00 L10 : Line)
    (C16 : Circle)
    (h00 : length_sum P18 P15 P30 P09 P16 P23)
    (h01 : angle_bisector_line P19 P29 P16 P27 L00)
    (h02 : between P19 P22 P25)
    (h03 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    (h04 : line_circle_intersection P19 L10 C16)
    : length_sum P30 P09 P18 P15 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1090
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1090

theorem v06_sealed_holdout_1091
    (P00 P04 P05 P12 P15 P16 P17 P18 P25 P26 P27 P29 P31 : Point)
    (h00 : equal_length P15 P26 P16 P27)
    (h01 : equal_length P16 P27 P05 P17)
    (h02 : between P26 P31 P04)
    (h03 : between P29 P12 P27)
    (h04 : midpoint P00 P25 P18)
    : equal_length P15 P26 P05 P17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1091
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1091

theorem v06_sealed_holdout_1092
    (P00 P02 P03 P04 P06 P07 P12 P13 P14 P16 P19 P21 P22 P23 P24 P26 P27 P29 P30 : Point)
    (L20 : Line)
    (h00 : area_eq P04 P30 P22 P02 P12 P23)
    (h01 : area_eq P02 P12 P23 P03 P13 P24)
    (h02 : angle_bisector_line P26 P00 P16 P27 L20)
    (h03 : between P04 P21 P06)
    (h04 : area_le P07 P02 P29 P24 P19 P14)
    : area_eq P04 P30 P22 P03 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1092
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1092

theorem v06_sealed_holdout_1093
    (P03 P04 P05 P08 P10 P11 P15 P16 P17 P23 P26 P27 P30 : Point)
    (L02 : Line)
    (C14 : Circle)
    (h00 : equal_length P17 P26 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : between P08 P17 P26)
    (h03 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h04 : line_circle_intersection P03 L02 C14)
    : equal_length P17 P26 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1093
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1093

theorem v06_sealed_holdout_1094
    (P01 P03 P05 P06 P07 P10 P11 P15 P16 P17 P18 P19 P24 P25 P26 P27 P28 : Point)
    (L02 L10 : Line)
    (C24 : Circle)
    (h00 : angle_bisector_line P07 P11 P25 P03 L02)
    (h01 : directed_angle_eq_mod_pi P15 P26 P05 P16 P27 P06)
    (h02 : area_le P18 P07 P28 P17 P06 P27)
    (h03 : line_circle_intersection P19 L10 C24)
    (h04 : area_le P24 P01 P10 P19 P28 P05)
    : angle_bisector P07 P11 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1094
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1094

theorem v06_sealed_holdout_1095
    (P02 P03 P04 P12 P16 P19 P22 P24 P25 P28 P31 : Point)
    (L00 L10 : Line)
    (C16 C18 C19 : Circle)
    (h00 : angle_bisector_line P03 P12 P24 P04 L00)
    (h01 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    (h02 : between P22 P03 P16)
    (h03 : line_circle_intersection P19 L10 C16)
    (h04 : circle_circle_intersection P03 C18 C19)
    : angle_bisector P03 P12 P24 P04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1095
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1095

theorem v06_sealed_holdout_1096
    (P01 P03 P04 P06 P07 P09 P12 P15 P16 P18 P19 P23 P24 P27 P30 P31 : Point)
    (L04 : Line)
    (C02 C18 : Circle)
    (h00 : directed_angle_eq_mod_pi P12 P19 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : angle_bisector_line P30 P01 P16 P27 L04)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : area_le P03 P06 P09 P12 P15 P18)
    : directed_angle_eq_mod_pi P12 P19 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1096
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1096

theorem v06_sealed_holdout_1097
    (P01 P02 P07 P10 P15 P16 P20 P21 P23 P25 P27 P29 P30 P31 : Point)
    (L16 : Line)
    (h00 : directed_angle_eq_mod_2pi P01 P23 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : angle_bisector_line P31 P01 P16 P27 L16)
    (h03 : between P07 P02 P29)
    (h04 : midpoint P10 P15 P20)
    : directed_angle_eq_mod_2pi P01 P23 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1097
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1097

theorem v06_sealed_holdout_1098
    (P00 P01 P04 P05 P07 P14 P15 P16 P19 P23 P24 P27 P31 : Point)
    (L24 L28 : Line)
    (C02 C22 : Circle)
    (h00 : directed_angle_eq_mod_pi P14 P19 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : angle_bisector_line P00 P01 P16 P27 L28)
    (h03 : angle_bisector_line P05 P04 P16 P27 L24)
    (h04 : circle_circle_intersection P19 C22 C02)
    : directed_angle_eq_mod_pi P14 P19 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1098
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1098

theorem v06_sealed_holdout_1099
    (P01 P02 P03 P07 P10 P16 P18 P19 P20 P21 P23 P24 P25 P28 P30 : Point)
    (h00 : directed_angle_eq_mod_2pi P03 P23 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : between P18 P07 P28)
    (h03 : midpoint P21 P20 P19)
    (h04 : midpoint P24 P01 P10)
    : directed_angle_eq_mod_2pi P03 P23 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1099
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1099

theorem v06_sealed_holdout_1100
    (P02 P03 P07 P10 P12 P16 P17 P21 P22 P23 P24 P25 P28 P29 P30 : Point)
    (L12 : Line)
    (C03 : Circle)
    (h00 : circle_through_three_noncollinear_points P24 P02 P16 C03)
    (h01 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    (h02 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h03 : midpoint P28 P29 P30)
    (h04 : angle_bisector_line P12 P07 P17 P28 L12)
    : triangle_pred P24 P02 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1100
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1100

theorem v06_sealed_holdout_1101
    (P00 P02 P03 P04 P06 P07 P08 P13 P16 P19 P26 P27 P30 P31 : Point)
    (L04 L28 : Line)
    (C02 C18 : Circle)
    (h00 : equilateral P13 P02 P06)
    (h01 : angle_bisector_line P30 P31 P16 P27 L04)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : angle_bisector_line P08 P04 P16 P27 L28)
    (h04 : directed_angle_eq_mod_pi P06 P19 P00 P13 P26 P07)
    : triangle_pred P13 P02 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1101
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1101

theorem v06_sealed_holdout_1102
    (P01 P02 P03 P04 P11 P13 P16 P26 P27 P28 P30 P31 : Point)
    (L12 L16 : Line)
    (C10 C17 C18 : Circle)
    (h00 : circle_through_three_noncollinear_points P26 P02 P16 C17)
    (h01 : angle_bisector_line P31 P30 P16 P27 L16)
    (h02 : angle_bisector_line P04 P01 P16 P27 L12)
    (h03 : circle_circle_intersection P03 C10 C18)
    (h04 : midpoint P13 P28 P11)
    : triangle_pred P26 P02 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1102
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1102

theorem v06_sealed_holdout_1103
    (P01 P02 P05 P06 P11 P15 P16 P17 P20 P22 P24 P27 P30 P31 : Point)
    (L24 : Line)
    (h00 : equilateral P15 P02 P06)
    (h01 : between P11 P30 P17)
    (h02 : angle_bisector_line P05 P01 P16 P27 L24)
    (h03 : between P17 P24 P31)
    (h04 : midpoint P20 P05 P22)
    : triangle_pred P15 P02 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1103
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1103

theorem v06_sealed_holdout_1104
    (P01 P02 P06 P07 P10 P16 P17 P18 P24 P27 P28 : Point)
    (L04 L28 : Line)
    (h00 : equilateral P16 P02 P06)
    (h01 : directed_angle_eq_mod_pi P18 P07 P28 P17 P06 P27)
    (h02 : angle_bisector_line P06 P01 P16 P27 L04)
    (h03 : between P24 P01 P10)
    (h04 : angle_bisector_line P16 P07 P17 P28 L28)
    : triangle_pred P16 P02 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1104
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1104

theorem v06_sealed_holdout_1105
    (P00 P03 P04 P08 P10 P11 P17 P19 P23 P25 P30 P31 : Point)
    (L02 : Line)
    (C14 : Circle)
    (h00 : P25 = P08)
    (h01 : P30 = P19)
    (h02 : P00 = P31)
    (h03 : area_le P11 P30 P17 P04 P23 P10)
    (h04 : line_circle_intersection P03 L02 C14)
    : rotation_preserves_collinear P25 P30 P00 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1105
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1105

theorem v06_sealed_holdout_1106
    (P00 P01 P03 P08 P19 P21 P31 : Point)
    (L26 : Line)
    (C10 C18 C20 : Circle)
    (h00 : P21 = P08)
    (h01 : P31 = P19)
    (h02 : P00 = P01)
    (h03 : line_circle_intersection P19 L26 C20)
    (h04 : circle_circle_intersection P03 C10 C18)
    : rotation_preserves_collinear P21 P31 P00 P08 P19 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1106
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1106

theorem v06_sealed_holdout_1107
    (P00 P03 P08 P16 P17 P19 P22 P25 P30 P31 : Point)
    (h00 : P17 = P08)
    (h01 : P00 = P19)
    (h02 : P30 = P31)
    (h03 : between P19 P22 P25)
    (h04 : between P22 P03 P16)
    : rotation_preserves_collinear P17 P00 P30 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1107
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1107

theorem v06_sealed_holdout_1108
    (P01 P03 P04 P08 P13 P18 P19 P23 P26 P29 P30 P31 : Point)
    (h00 : P13 = P08)
    (h01 : P01 = P19)
    (h02 : P29 = P31)
    (h03 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    (h04 : between P26 P31 P04)
    : rotation_preserves_collinear P13 P01 P29 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1108
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1108

theorem v06_sealed_holdout_1109
    (P01 P02 P03 P08 P09 P14 P19 P27 P28 P31 : Point)
    (L02 : Line)
    (C14 : Circle)
    (h00 : P09 = P08)
    (h01 : P02 = P19)
    (h02 : P28 = P31)
    (h03 : between P27 P14 P01)
    (h04 : line_circle_intersection P03 L02 C14)
    : rotation_preserves_collinear P09 P02 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1109
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1109

theorem v06_sealed_holdout_1110
    (P00 P01 P02 P03 P04 P05 P12 P18 P19 P20 P23 P28 P29 P30 : Point)
    (L26 : Line)
    (C15 C20 : Circle)
    (h00 : circle_with_center_through_point P18 P20 C15)
    (h01 : midpoint P28 P29 P30)
    (h02 : line_circle_intersection P19 L26 C20)
    (h03 : midpoint P02 P23 P12)
    (h04 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    : on_circle P20 C15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1110
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1110

theorem v06_sealed_holdout_1111
    (P01 P02 P05 P06 P12 P13 P14 P15 P19 P24 P26 P28 P29 P30 : Point)
    (L04 L08 L30 : Line)
    (C06 : Circle)
    (h00 : tangent_chord_angle P30 P24 P29 L30 C06)
    (h01 : between P12 P13 P14)
    (h02 : midpoint P15 P26 P05)
    (h03 : angle_bisector_line P01 P02 P19 P28 L08)
    (h04 : angle_bisector_line P06 P05 P19 P28 L04)
    : on_circle P29 C06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1111
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1111

theorem v06_sealed_holdout_1112
    (P02 P03 P18 P19 P22 P25 P26 P28 P29 P31 : Point)
    (L10 L18 L24 : Line)
    (C02 C16 C18 C22 : Circle)
    (h00 : tangent_chord_angle P26 P25 P28 L18 C22)
    (h01 : circle_circle_intersection P03 C02 C18)
    (h02 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    (h03 : angle_bisector_line P29 P03 P18 P28 L24)
    (h04 : line_circle_intersection P19 L10 C16)
    : on_circle P28 C22 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1112
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1112

theorem v06_sealed_holdout_1113
    (P03 P08 P10 P12 P15 P19 P23 P25 P27 P28 P29 : Point)
    (L02 L27 : Line)
    (C02 C18 C22 C30 : Circle)
    (h00 : altitude P28 P03 P15 P23 L27)
    (h01 : line_circle_intersection P03 L02 C22)
    (h02 : area_le P29 P12 P27 P10 P25 P08)
    (h03 : circle_circle_intersection P03 C02 C18)
    (h04 : circle_circle_intersection P19 C30 C02)
    : on_line P15 L27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1113
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1113

theorem v06_sealed_holdout_1114
    (P04 P06 P07 P08 P10 P15 P17 P19 P20 P21 P23 P25 P29 : Point)
    (L10 L12 L26 : Line)
    (C00 C04 : Circle)
    (h00 : angle_bisector_line P17 P07 P21 P29 L12)
    (h01 : line_circle_intersection P19 L10 C00)
    (h02 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    (h03 : line_circle_intersection P19 L26 C04)
    (h04 : between P10 P15 P20)
    : on_line P17 L12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1114
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1114

theorem v06_sealed_holdout_1115
    (P02 P03 P04 P05 P07 P08 P10 P11 P13 P14 P17 P20 P23 P26 P29 P30 P31 : Point)
    (L08 : Line)
    (h00 : angle_bisector_line P13 P07 P20 P29 L08)
    (h01 : midpoint P05 P04 P03)
    (h02 : midpoint P08 P17 P26)
    (h03 : area_le P11 P30 P17 P04 P23 P10)
    (h04 : area_le P14 P11 P08 P05 P02 P31)
    : on_line P13 L08 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1115
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1115

theorem v06_sealed_holdout_1116
    (P03 P05 P06 P08 P09 P12 P13 P14 P15 P16 P17 P19 P26 P27 P29 : Point)
    (L02 L04 L10 : Line)
    (C06 C16 : Circle)
    (h00 : angle_bisector_line P09 P08 P19 P29 L04)
    (h01 : line_circle_intersection P19 L10 C16)
    (h02 : directed_angle_eq_mod_pi P12 P13 P14 P15 P16 P17)
    (h03 : area_le P15 P26 P05 P16 P27 P06)
    (h04 : line_circle_intersection P03 L02 C06)
    : on_line P09 L04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1116
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1116

theorem v06_sealed_holdout_1117
    (P02 P03 P19 P29 : Point)
    (L02 L18 : Line)
    (C02 C22 C30 : Circle)
    (h00 : equilateral P19 P29 P02)
    (h01 : circle_circle_intersection P19 C30 C02)
    (h02 : line_circle_intersection P03 L02 C30)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : line_circle_intersection P03 L18 C02)
    : equal_length P19 P29 P29 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1117
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1117

theorem v06_sealed_holdout_1118
    (P01 P03 P04 P07 P13 P15 P18 P19 P23 P26 P28 P30 P31 : Point)
    (L00 L10 : Line)
    (C08 : Circle)
    (h00 : equilateral P15 P30 P01)
    (h01 : between P23 P18 P13)
    (h02 : between P26 P31 P04)
    (h03 : line_circle_intersection P19 L10 C08)
    (h04 : angle_bisector_line P03 P07 P18 P28 L00)
    : equal_length P15 P30 P30 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1118
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1118

theorem v06_sealed_holdout_1119
    (P00 P01 P03 P11 P14 P15 P18 P19 P21 P24 P27 P30 P31 : Point)
    (L10 : Line)
    (C00 C18 C19 : Circle)
    (h00 : equilateral P11 P31 P00)
    (h01 : between P27 P14 P01)
    (h02 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    (h03 : line_circle_intersection P19 L10 C00)
    (h04 : circle_circle_intersection P03 C18 C19)
    : equal_length P11 P31 P31 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1119
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1119

theorem v06_sealed_holdout_1120
    (P00 P01 P02 P03 P04 P05 P09 P10 P11 P12 P16 P17 P18 P22 P23 P30 : Point)
    (L18 : Line)
    (C10 : Circle)
    (h00 : length_sum P16 P17 P30 P09 P18 P23)
    (h01 : area_le P02 P23 P12 P01 P22 P11)
    (h02 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    (h03 : line_circle_intersection P03 L18 C10)
    (h04 : area_le P11 P30 P17 P04 P23 P10)
    : length_sum P30 P09 P16 P17 P18 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1120
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1120

theorem v06_sealed_holdout_1121
    (P03 P05 P06 P12 P13 P14 P15 P16 P17 P26 P27 P28 : Point)
    (C10 C18 : Circle)
    (h00 : equal_length P13 P27 P16 P28)
    (h01 : equal_length P16 P28 P05 P15)
    (h02 : area_le P12 P13 P14 P15 P16 P17)
    (h03 : area_le P15 P26 P05 P16 P27 P06)
    (h04 : circle_circle_intersection P03 C10 C18)
    : equal_length P13 P27 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1121
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1121

theorem v06_sealed_holdout_1122
    (P02 P03 P04 P07 P12 P13 P16 P19 P21 P22 P23 P24 P25 P30 P31 : Point)
    (L02 : Line)
    (C30 : Circle)
    (h00 : area_eq P02 P31 P22 P03 P12 P23)
    (h01 : area_eq P03 P12 P23 P04 P13 P24)
    (h02 : between P19 P22 P25)
    (h03 : line_circle_intersection P03 L02 C30)
    (h04 : area_le P25 P16 P07 P30 P21 P12)
    : area_eq P02 P31 P22 P04 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1122
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1122

theorem v06_sealed_holdout_1123
    (P00 P03 P05 P15 P16 P17 P18 P25 P27 P28 P30 : Point)
    (L02 L04 : Line)
    (C22 : Circle)
    (h00 : equal_length P15 P27 P16 P28)
    (h01 : equal_length P16 P28 P05 P17)
    (h02 : line_circle_intersection P03 L02 C22)
    (h03 : angle_bisector_line P30 P05 P16 P27 L04)
    (h04 : midpoint P00 P25 P18)
    : equal_length P15 P27 P05 P17 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1123
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1123

theorem v06_sealed_holdout_1124
    (P01 P03 P04 P05 P08 P10 P12 P15 P17 P20 P22 P25 P28 P29 P31 : Point)
    (L04 L12 L16 : Line)
    (h00 : angle_bisector_line P05 P12 P25 P03 L04)
    (h01 : directed_angle_eq_mod_pi P01 P08 P15 P22 P29 P04)
    (h02 : angle_bisector_line P31 P01 P17 P28 L16)
    (h03 : angle_bisector_line P04 P05 P17 P28 L12)
    (h04 : between P10 P15 P20)
    : angle_bisector P05 P12 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1124
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1124

theorem v06_sealed_holdout_1125
    (P00 P01 P02 P03 P05 P08 P11 P13 P14 P16 P17 P22 P24 P26 P27 P30 P31 : Point)
    (L02 L04 L28 : Line)
    (h00 : angle_bisector_line P01 P13 P24 P03 L02)
    (h01 : angle_bisector_line P22 P30 P16 P27 L04)
    (h02 : between P08 P17 P26)
    (h03 : angle_bisector_line P00 P05 P16 P27 L28)
    (h04 : area_le P14 P11 P08 P05 P02 P31)
    : angle_bisector P01 P13 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1125
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1125

theorem v06_sealed_holdout_1126
    (P01 P04 P05 P06 P07 P10 P15 P16 P17 P18 P19 P20 P21 P23 P24 P26 P27 P31 : Point)
    (L08 : Line)
    (h00 : directed_angle_eq_mod_pi P10 P20 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : area_le P15 P26 P05 P16 P27 P06)
    (h03 : angle_bisector_line P01 P05 P16 P27 L08)
    (h04 : area_le P21 P20 P19 P18 P17 P16)
    : directed_angle_eq_mod_pi P10 P20 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1126
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1126

theorem v06_sealed_holdout_1127
    (P02 P07 P10 P12 P16 P21 P24 P25 P27 P28 P29 P30 P31 : Point)
    (L24 : Line)
    (h00 : directed_angle_eq_mod_2pi P31 P24 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : angle_bisector_line P29 P02 P16 P27 L24)
    (h03 : area_le P25 P16 P07 P30 P21 P12)
    (h04 : between P28 P29 P30)
    : directed_angle_eq_mod_2pi P31 P24 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1127
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1127

theorem v06_sealed_holdout_1128
    (P00 P04 P07 P08 P09 P11 P12 P15 P16 P17 P18 P19 P20 P23 P24 P25 P28 P29 P31 : Point)
    (L28 : Line)
    (C02 C06 : Circle)
    (h00 : directed_angle_eq_mod_pi P12 P20 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : circle_circle_intersection P19 C06 C02)
    (h03 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    (h04 : angle_bisector_line P08 P09 P17 P28 L28)
    : directed_angle_eq_mod_pi P12 P20 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1128
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1128

theorem v06_sealed_holdout_1129
    (P01 P02 P03 P04 P06 P07 P08 P10 P14 P15 P16 P19 P20 P21 P23 P24 P25 P29 P30 : Point)
    (h00 : directed_angle_eq_mod_2pi P01 P24 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : area_le P04 P21 P06 P23 P08 P25)
    (h03 : area_le P07 P02 P29 P24 P19 P14)
    (h04 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    : directed_angle_eq_mod_2pi P01 P24 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1129
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1129

theorem v06_sealed_holdout_1130
    (P00 P02 P03 P05 P06 P08 P11 P13 P14 P16 P17 P20 P22 P24 P26 P27 P31 : Point)
    (L28 : Line)
    (C21 : Circle)
    (h00 : circle_through_three_noncollinear_points P22 P03 P16 C21)
    (h01 : midpoint P08 P17 P26)
    (h02 : angle_bisector_line P00 P02 P16 P27 L28)
    (h03 : directed_angle_eq_mod_pi P14 P11 P08 P05 P02 P31)
    (h04 : area_le P17 P24 P31 P06 P13 P20)
    : triangle_pred P22 P03 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1130
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1130

theorem v06_sealed_holdout_1131
    (P01 P03 P05 P06 P10 P11 P15 P16 P19 P24 P26 P27 P28 : Point)
    (L02 : Line)
    (C02 C06 : Circle)
    (h00 : equilateral P11 P03 P06)
    (h01 : area_le P15 P26 P05 P16 P27 P06)
    (h02 : line_circle_intersection P03 L02 C06)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : area_le P24 P01 P10 P19 P28 P05)
    : triangle_pred P11 P03 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1131
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1131

theorem v06_sealed_holdout_1132
    (P03 P10 P16 P19 P21 P22 P24 P28 P29 P30 P31 : Point)
    (C02 C03 C22 : Circle)
    (h00 : circle_through_three_noncollinear_points P24 P03 P16 C03)
    (h01 : midpoint P22 P03 P16)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : between P28 P29 P30)
    (h04 : midpoint P31 P10 P21)
    : triangle_pred P24 P03 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1132
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1132

theorem v06_sealed_holdout_1133
    (P00 P03 P04 P06 P11 P12 P13 P18 P19 P25 P27 P29 : Point)
    (L26 : Line)
    (C12 C18 C26 : Circle)
    (h00 : equilateral P13 P03 P06)
    (h01 : between P29 P12 P27)
    (h02 : area_le P00 P25 P18 P11 P04 P29)
    (h03 : line_circle_intersection P19 L26 C12)
    (h04 : circle_circle_intersection P03 C26 C18)
    : triangle_pred P13 P03 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1133
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1133

theorem v06_sealed_holdout_1134
    (P02 P03 P06 P07 P11 P13 P14 P28 P29 : Point)
    (L02 L18 : Line)
    (C18 C22 : Circle)
    (h00 : equilateral P14 P03 P06)
    (h01 : line_circle_intersection P03 L18 C18)
    (h02 : between P07 P02 P29)
    (h03 : line_circle_intersection P03 L02 C22)
    (h04 : between P13 P28 P11)
    : triangle_pred P14 P03 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1134
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1134

theorem v06_sealed_holdout_1135
    (P00 P01 P03 P08 P12 P19 P23 P27 P29 P31 : Point)
    (L18 : Line)
    (C26 : Circle)
    (h00 : P23 = P08)
    (h01 : P31 = P19)
    (h02 : P00 = P01)
    (h03 : midpoint P29 P12 P27)
    (h04 : line_circle_intersection P03 L18 C26)
    : rotation_preserves_collinear P23 P31 P00 P08 P19 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1135
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1135

theorem v06_sealed_holdout_1136
    (P00 P01 P06 P08 P15 P19 P20 P28 P31 : Point)
    (L16 : Line)
    (h00 : P19 = P08)
    (h01 : P00 = P20)
    (h02 : P31 = P01)
    (h03 : midpoint P01 P08 P15)
    (h04 : angle_bisector_line P31 P06 P19 P28 L16)
    : rotation_preserves_collinear P19 P00 P31 P08 P20 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1136
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1136

theorem v06_sealed_holdout_1137
    (P01 P03 P04 P05 P08 P15 P17 P19 P26 P30 P31 : Point)
    (h00 : P15 = P08)
    (h01 : P01 = P19)
    (h02 : P30 = P31)
    (h03 : between P05 P04 P03)
    (h04 : midpoint P08 P17 P26)
    : rotation_preserves_collinear P15 P01 P30 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1137
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1137

theorem v06_sealed_holdout_1138
    (P02 P07 P08 P11 P18 P19 P23 P28 P29 P31 : Point)
    (L10 L16 : Line)
    (C16 : Circle)
    (h00 : P11 = P08)
    (h01 : P02 = P19)
    (h02 : P29 = P31)
    (h03 : line_circle_intersection P19 L10 C16)
    (h04 : angle_bisector_line P23 P07 P18 P28 L16)
    : rotation_preserves_collinear P11 P02 P29 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1138
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1138

theorem v06_sealed_holdout_1139
    (P03 P07 P08 P09 P11 P13 P19 P24 P26 P28 P31 : Point)
    (L18 : Line)
    (C26 : Circle)
    (h00 : P07 = P08)
    (h01 : P03 = P19)
    (h02 : P28 = P31)
    (h03 : directed_angle_eq_mod_pi P13 P28 P11 P26 P09 P24)
    (h04 : line_circle_intersection P03 L18 C26)
    : rotation_preserves_collinear P07 P03 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1139
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1139

theorem v06_sealed_holdout_1140
    (P03 P04 P05 P08 P09 P13 P14 P18 P19 P20 P22 P23 P24 P26 P30 P31 : Point)
    (L10 : Line)
    (C00 C27 : Circle)
    (h00 : circle_through_three_noncollinear_points P09 P24 P31 C27)
    (h01 : line_circle_intersection P19 L10 C00)
    (h02 : midpoint P20 P05 P22)
    (h03 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    (h04 : area_le P26 P31 P04 P09 P14 P19)
    : on_circle P09 C27 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1140
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1140

theorem v06_sealed_holdout_1141
    (P01 P02 P03 P07 P08 P15 P25 P28 P29 : Point)
    (L10 L18 : Line)
    (C10 C18 C26 : Circle)
    (h00 : tangent_chord_angle P28 P25 P29 L10 C10)
    (h01 : circle_circle_intersection P03 C26 C18)
    (h02 : between P01 P08 P15)
    (h03 : line_circle_intersection P03 L18 C18)
    (h04 : between P07 P02 P29)
    : on_circle P29 C10 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1141
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1141

theorem v06_sealed_holdout_1142
    (P03 P04 P05 P06 P10 P11 P17 P19 P23 P28 P30 : Point)
    (L05 L24 : Line)
    (C02 C04 C18 : Circle)
    (h00 : line_circle_intersection P05 L05 C04)
    (h01 : between P05 P04 P03)
    (h02 : circle_circle_intersection P03 C02 C18)
    (h03 : area_le P11 P30 P17 P04 P23 P10)
    (h04 : angle_bisector_line P05 P06 P19 P28 L24)
    : on_line P05 L05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1142
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1142

theorem v06_sealed_holdout_1143
    (P00 P01 P03 P05 P06 P07 P09 P15 P16 P17 P18 P23 P26 P27 P28 : Point)
    (L03 : Line)
    (C04 C18 C19 : Circle)
    (h00 : line_circle_intersection P01 L03 C04)
    (h01 : midpoint P09 P00 P23)
    (h02 : circle_circle_intersection P03 C18 C19)
    (h03 : area_le P15 P26 P05 P16 P27 P06)
    (h04 : area_le P18 P07 P28 P17 P06 P27)
    : on_line P01 L03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1143
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1143

theorem v06_sealed_holdout_1144
    (P02 P03 P06 P07 P08 P10 P12 P15 P16 P19 P21 P22 P23 P25 P28 P29 P30 P31 : Point)
    (L16 : Line)
    (h00 : angle_bisector_line P15 P08 P21 P29 L16)
    (h01 : area_le P19 P22 P25 P28 P31 P02)
    (h02 : area_le P22 P03 P16 P29 P10 P23)
    (h03 : area_le P25 P16 P07 P30 P21 P12)
    (h04 : angle_bisector_line P07 P06 P19 P28 L16)
    : on_line P15 L16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1144
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1144

theorem v06_sealed_holdout_1145
    (P03 P04 P08 P11 P13 P18 P19 P20 P23 P26 P29 P31 : Point)
    (L12 L18 : Line)
    (C02 C06 C26 : Circle)
    (h00 : angle_bisector_line P11 P08 P20 P29 L12)
    (h01 : midpoint P23 P18 P13)
    (h02 : midpoint P26 P31 P04)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : line_circle_intersection P03 L18 C26)
    : on_line P11 L12 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1145
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1145

theorem v06_sealed_holdout_1146
    (P01 P04 P06 P07 P08 P09 P14 P15 P18 P19 P21 P24 P27 P29 P30 : Point)
    (L08 : Line)
    (h00 : angle_bisector_line P07 P09 P19 P29 L08)
    (h01 : between P27 P14 P01)
    (h02 : area_le P30 P27 P24 P21 P18 P15)
    (h03 : between P01 P08 P15)
    (h04 : between P04 P21 P06)
    : on_line P07 L08 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1146
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1146

theorem v06_sealed_holdout_1147
    (P00 P01 P02 P03 P04 P05 P08 P17 P19 P26 P30 : Point)
    (L02 L26 : Line)
    (C14 C28 : Circle)
    (h00 : equilateral P17 P30 P02)
    (h01 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    (h02 : between P08 P17 P26)
    (h03 : line_circle_intersection P19 L26 C28)
    (h04 : line_circle_intersection P03 L02 C14)
    : equal_length P17 P30 P30 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1147
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1147

theorem v06_sealed_holdout_1148
    (P00 P01 P05 P06 P08 P09 P13 P14 P15 P16 P17 P18 P23 P26 P27 P28 P31 : Point)
    (L08 L16 : Line)
    (h00 : equilateral P13 P31 P01)
    (h01 : directed_angle_eq_mod_pi P09 P00 P23 P14 P05 P28)
    (h02 : angle_bisector_line P23 P01 P17 P28 L16)
    (h03 : area_le P15 P26 P05 P16 P27 P06)
    (h04 : angle_bisector_line P01 P08 P18 P28 L08)
    : equal_length P13 P31 P31 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1148
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1148

theorem v06_sealed_holdout_1149
    (P00 P01 P02 P03 P09 P10 P16 P19 P22 P23 P29 : Point)
    (L26 : Line)
    (C02 C06 C12 : Circle)
    (h00 : equilateral P09 P00 P01)
    (h01 : circle_circle_intersection P19 C06 C02)
    (h02 : between P16 P09 P02)
    (h03 : line_circle_intersection P19 L26 C12)
    (h04 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    : equal_length P09 P00 P00 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1149
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1149

theorem v06_sealed_holdout_1150
    (P03 P05 P07 P08 P09 P13 P14 P16 P17 P18 P19 P20 P22 P23 P24 P25 P27 P30 : Point)
    (L08 L10 : Line)
    (C08 : Circle)
    (h00 : length_sum P14 P17 P30 P09 P16 P23)
    (h01 : directed_angle_eq_mod_pi P20 P05 P22 P07 P24 P09)
    (h02 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    (h03 : angle_bisector_line P25 P05 P16 P27 L08)
    (h04 : line_circle_intersection P19 L10 C08)
    : length_sum P30 P09 P14 P17 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1150
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1150

theorem v06_sealed_holdout_1151
    (P04 P05 P06 P08 P11 P15 P16 P18 P19 P21 P23 P24 P25 P27 P28 P30 : Point)
    (L10 : Line)
    (C00 : Circle)
    (h00 : equal_length P11 P28 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : area_le P30 P27 P24 P21 P18 P15)
    (h03 : line_circle_intersection P19 L10 C00)
    (h04 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    : equal_length P11 P28 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1151
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1151

theorem v06_sealed_holdout_1152
    (P00 P01 P02 P03 P08 P12 P13 P17 P19 P22 P23 P24 P26 : Point)
    (L10 : Line)
    (C02 C24 C30 : Circle)
    (h00 : area_eq P00 P01 P22 P02 P12 P23)
    (h01 : area_eq P02 P12 P23 P03 P13 P24)
    (h02 : line_circle_intersection P19 L10 C24)
    (h03 : between P08 P17 P26)
    (h04 : circle_circle_intersection P19 C30 C02)
    : area_eq P00 P01 P22 P03 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1152
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1152

theorem v06_sealed_holdout_1153
    (P03 P05 P13 P15 P16 P27 P28 : Point)
    (L02 L12 : Line)
    (C06 C18 C19 : Circle)
    (h00 : equal_length P13 P28 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : circle_circle_intersection P03 C18 C19)
    (h03 : angle_bisector_line P28 P05 P16 P27 L12)
    (h04 : line_circle_intersection P03 L02 C06)
    : equal_length P13 P28 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1153
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1153

theorem v06_sealed_holdout_1154
    (P03 P04 P13 P19 P22 P25 P28 P29 P30 : Point)
    (L02 L06 : Line)
    (C02 C22 C30 : Circle)
    (h00 : angle_bisector_line P03 P13 P25 P04 L06)
    (h01 : between P19 P22 P25)
    (h02 : line_circle_intersection P03 L02 C30)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : between P28 P29 P30)
    : angle_bisector P03 P13 P25 P04 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1154
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1154

theorem v06_sealed_holdout_1155
    (P03 P04 P12 P14 P19 P24 P26 P27 P29 P31 : Point)
    (L04 L18 L26 : Line)
    (C04 C26 : Circle)
    (h00 : angle_bisector_line P31 P14 P24 P03 L04)
    (h01 : line_circle_intersection P19 L26 C04)
    (h02 : midpoint P26 P31 P04)
    (h03 : between P29 P12 P27)
    (h04 : line_circle_intersection P03 L18 C26)
    : angle_bisector P31 P14 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1155
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1155

theorem v06_sealed_holdout_1156
    (P02 P04 P06 P07 P08 P15 P16 P21 P23 P24 P26 P27 P29 P31 : Point)
    (L20 : Line)
    (h00 : directed_angle_eq_mod_pi P08 P21 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : angle_bisector_line P26 P02 P16 P27 L20)
    (h03 : midpoint P04 P21 P06)
    (h04 : between P07 P02 P29)
    : directed_angle_eq_mod_pi P08 P21 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1156
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1156

theorem v06_sealed_holdout_1157
    (P02 P03 P04 P07 P08 P10 P11 P12 P16 P17 P21 P23 P25 P26 P29 P30 : Point)
    (C18 C26 : Circle)
    (h00 : directed_angle_eq_mod_2pi P29 P25 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P26 P02)
    (h02 : directed_angle_eq_mod_pi P08 P17 P26 P03 P12 P21)
    (h03 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h04 : circle_circle_intersection P03 C26 C18)
    : directed_angle_eq_mod_2pi P29 P25 P10 P16 P26 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1157
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1157

theorem v06_sealed_holdout_1158
    (P01 P04 P06 P07 P10 P15 P16 P17 P18 P19 P20 P21 P23 P24 P27 P31 : Point)
    (L08 L26 : Line)
    (C20 : Circle)
    (h00 : directed_angle_eq_mod_pi P10 P21 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : line_circle_intersection P19 L26 C20)
    (h03 : angle_bisector_line P01 P06 P16 P27 L08)
    (h04 : area_le P21 P20 P19 P18 P17 P16)
    : directed_angle_eq_mod_pi P10 P21 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1158
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1158

theorem v06_sealed_holdout_1159
    (P02 P03 P07 P10 P12 P16 P21 P22 P23 P25 P26 P28 P29 P30 P31 : Point)
    (h00 : directed_angle_eq_mod_2pi P31 P25 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P26 P02)
    (h02 : area_le P22 P03 P16 P29 P10 P23)
    (h03 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    (h04 : between P28 P29 P30)
    : directed_angle_eq_mod_2pi P31 P25 P10 P16 P26 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1159
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1159

theorem v06_sealed_holdout_1160
    (P00 P03 P04 P06 P09 P11 P12 P16 P18 P20 P25 P27 P29 P31 : Point)
    (L08 : Line)
    (C07 : Circle)
    (h00 : circle_through_three_noncollinear_points P20 P04 P16 C07)
    (h01 : angle_bisector_line P25 P31 P16 P27 L08)
    (h02 : between P29 P12 P27)
    (h03 : directed_angle_eq_mod_pi P00 P25 P18 P11 P04 P29)
    (h04 : midpoint P03 P06 P09)
    : triangle_pred P20 P04 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1160
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1160

theorem v06_sealed_holdout_1161
    (P01 P02 P03 P04 P06 P07 P08 P09 P10 P14 P15 P19 P20 P21 P23 P24 P25 P29 P30 : Point)
    (h00 : equilateral P09 P04 P06)
    (h01 : between P01 P08 P15)
    (h02 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    (h03 : area_le P07 P02 P29 P24 P19 P14)
    (h04 : directed_angle_eq_mod_pi P10 P15 P20 P25 P30 P03)
    : triangle_pred P09 P04 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1161
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1161

theorem v06_sealed_holdout_1162
    (P03 P04 P06 P10 P11 P13 P16 P17 P20 P22 P23 P24 P30 P31 : Point)
    (L02 L18 : Line)
    (C10 C14 C21 : Circle)
    (h00 : circle_through_three_noncollinear_points P22 P04 P16 C21)
    (h01 : line_circle_intersection P03 L18 C10)
    (h02 : area_le P11 P30 P17 P04 P23 P10)
    (h03 : line_circle_intersection P03 L02 C14)
    (h04 : area_le P17 P24 P31 P06 P13 P20)
    : triangle_pred P22 P04 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1162
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1162

theorem v06_sealed_holdout_1163
    (P01 P04 P05 P06 P07 P10 P11 P15 P16 P18 P19 P24 P26 P27 P28 : Point)
    (C02 C06 : Circle)
    (h00 : equilateral P11 P04 P06)
    (h01 : area_le P15 P26 P05 P16 P27 P06)
    (h02 : midpoint P18 P07 P28)
    (h03 : circle_circle_intersection P19 C06 C02)
    (h04 : between P24 P01 P10)
    : triangle_pred P11 P04 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1163
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1163

theorem v06_sealed_holdout_1164
    (P00 P03 P04 P06 P10 P11 P12 P19 P21 P22 P28 P29 P30 P31 : Point)
    (L02 : Line)
    (C02 C22 C30 : Circle)
    (h00 : equilateral P12 P04 P06)
    (h01 : line_circle_intersection P03 L02 C30)
    (h02 : circle_circle_intersection P19 C22 C02)
    (h03 : midpoint P28 P29 P30)
    (h04 : area_le P31 P10 P21 P00 P11 P22)
    : triangle_pred P12 P04 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1164
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1164

theorem v06_sealed_holdout_1165
    (P00 P01 P07 P08 P18 P19 P21 P28 P31 : Point)
    (C02 C14 : Circle)
    (h00 : P21 = P08)
    (h01 : P00 = P19)
    (h02 : P01 = P31)
    (h03 : circle_circle_intersection P19 C14 C02)
    (h04 : between P18 P07 P28)
    : rotation_preserves_collinear P21 P00 P01 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1165
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1165

theorem v06_sealed_holdout_1166
    (P00 P01 P03 P08 P16 P17 P19 P22 P25 P31 : Point)
    (h00 : P17 = P08)
    (h01 : P01 = P19)
    (h02 : P31 = P00)
    (h03 : midpoint P19 P22 P25)
    (h04 : midpoint P22 P03 P16)
    : rotation_preserves_collinear P17 P01 P31 P08 P19 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1166
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1166

theorem v06_sealed_holdout_1167
    (P02 P03 P04 P08 P09 P13 P14 P18 P19 P23 P26 P30 P31 : Point)
    (h00 : P13 = P08)
    (h01 : P02 = P19)
    (h02 : P30 = P31)
    (h03 : directed_angle_eq_mod_pi P23 P18 P13 P08 P03 P30)
    (h04 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    : rotation_preserves_collinear P13 P02 P30 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1167
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1167

theorem v06_sealed_holdout_1168
    (P03 P05 P08 P09 P16 P17 P19 P28 P29 P31 : Point)
    (L28 : Line)
    (C18 C26 : Circle)
    (h00 : P09 = P08)
    (h01 : P03 = P19)
    (h02 : P29 = P31)
    (h03 : angle_bisector_line P16 P05 P17 P28 L28)
    (h04 : circle_circle_intersection P03 C26 C18)
    : rotation_preserves_collinear P09 P03 P29 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1168
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1168

theorem v06_sealed_holdout_1169
    (P00 P03 P04 P05 P08 P10 P11 P19 P21 P22 P28 P31 : Point)
    (C10 C18 : Circle)
    (h00 : P05 = P08)
    (h01 : P04 = P19)
    (h02 : P28 = P31)
    (h03 : area_le P31 P10 P21 P00 P11 P22)
    (h04 : circle_circle_intersection P03 C10 C18)
    : rotation_preserves_collinear P05 P04 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1169
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1169

theorem v06_sealed_holdout_1170
    (P00 P03 P06 P09 P14 P18 P19 P22 P23 P25 : Point)
    (C23 : Circle)
    (h00 : circle_with_center_through_point P14 P22 C23)
    (h01 : midpoint P00 P25 P18)
    (h02 : midpoint P03 P06 P09)
    (h03 : between P06 P19 P00)
    (h04 : between P09 P00 P23)
    : on_circle P22 C23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1170
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1170

theorem v06_sealed_holdout_1171
    (P02 P03 P09 P16 P19 P22 P26 P27 P29 : Point)
    (L10 L22 L26 : Line)
    (C12 C14 C16 : Circle)
    (h00 : tangent_chord_angle P26 P27 P29 L22 C14)
    (h01 : midpoint P16 P09 P02)
    (h02 : line_circle_intersection P19 L26 C12)
    (h03 : between P22 P03 P16)
    (h04 : line_circle_intersection P19 L10 C16)
    : on_circle P29 C14 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1171
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1171

theorem v06_sealed_holdout_1172
    (P03 P04 P09 P12 P14 P19 P22 P26 P27 P28 P29 P31 : Point)
    (L10 L26 : Line)
    (C04 C18 C19 C30 : Circle)
    (h00 : tangent_chord_angle P22 P27 P28 L10 C30)
    (h01 : circle_circle_intersection P03 C18 C19)
    (h02 : line_circle_intersection P19 L26 C04)
    (h03 : area_le P26 P31 P04 P09 P14 P19)
    (h04 : midpoint P29 P12 P27)
    : on_circle P28 C30 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1172
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1172

theorem v06_sealed_holdout_1173
    (P01 P04 P08 P15 P18 P19 P21 P22 P24 P27 P28 P29 P30 P31 : Point)
    (L05 L16 : Line)
    (C02 C20 C30 : Circle)
    (h00 : line_circle_intersection P31 L05 C20)
    (h01 : circle_circle_intersection P19 C30 C02)
    (h02 : area_le P30 P27 P24 P21 P18 P15)
    (h03 : directed_angle_eq_mod_pi P01 P08 P15 P22 P29 P04)
    (h04 : angle_bisector_line P31 P08 P19 P28 L16)
    : on_line P31 L05 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1173
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1173

theorem v06_sealed_holdout_1174
    (P00 P01 P02 P03 P04 P05 P08 P11 P12 P13 P17 P21 P26 P29 P30 : Point)
    (L20 : Line)
    (C18 C26 : Circle)
    (h00 : angle_bisector_line P13 P08 P21 P29 L20)
    (h01 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    (h02 : area_le P08 P17 P26 P03 P12 P21)
    (h03 : between P11 P30 P17)
    (h04 : circle_circle_intersection P03 C26 C18)
    : on_line P13 L20 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1174
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1174

theorem v06_sealed_holdout_1175
    (P03 P05 P06 P07 P09 P10 P15 P17 P18 P19 P20 P26 P27 P28 P29 : Point)
    (L16 L18 : Line)
    (C02 C22 : Circle)
    (h00 : angle_bisector_line P09 P10 P20 P29 L16)
    (h01 : circle_circle_intersection P19 C22 C02)
    (h02 : line_circle_intersection P03 L18 C02)
    (h03 : between P15 P26 P05)
    (h04 : area_le P18 P07 P28 P17 P06 P27)
    : on_line P09 L16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1175
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1175

theorem v06_sealed_holdout_1176
    (P02 P03 P07 P10 P12 P16 P19 P21 P22 P23 P25 P28 P29 P30 P31 : Point)
    (L18 : Line)
    (C12 C26 : Circle)
    (h00 : line_circle_intersection P02 L18 C12)
    (h01 : line_circle_intersection P03 L18 C26)
    (h02 : area_le P19 P22 P25 P28 P31 P02)
    (h03 : directed_angle_eq_mod_pi P22 P03 P16 P29 P10 P23)
    (h04 : directed_angle_eq_mod_pi P25 P16 P07 P30 P21 P12)
    : on_line P02 L18 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1176
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1176

theorem v06_sealed_holdout_1177
    (P00 P01 P02 P03 P08 P12 P13 P15 P18 P23 P25 P27 P28 P29 P30 P31 : Point)
    (L08 : Line)
    (h00 : equilateral P15 P31 P02)
    (h01 : area_le P23 P18 P13 P08 P03 P30)
    (h02 : angle_bisector_line P25 P01 P18 P28 L08)
    (h03 : between P29 P12 P27)
    (h04 : between P00 P25 P18)
    : equal_length P15 P31 P31 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1177
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1177

theorem v06_sealed_holdout_1178
    (P00 P01 P02 P04 P06 P08 P11 P15 P17 P19 P21 P23 P25 P28 : Point)
    (L24 : Line)
    (C02 C30 : Circle)
    (h00 : equilateral P11 P00 P01)
    (h01 : circle_circle_intersection P19 C30 C02)
    (h02 : angle_bisector_line P21 P02 P17 P28 L24)
    (h03 : between P01 P08 P15)
    (h04 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    : equal_length P11 P00 P00 P01 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1178
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1178

theorem v06_sealed_holdout_1179
    (P00 P01 P02 P03 P04 P05 P07 P08 P10 P12 P17 P21 P23 P26 P31 : Point)
    (h00 : equilateral P07 P01 P00)
    (h01 : midpoint P31 P10 P21)
    (h02 : midpoint P02 P23 P12)
    (h03 : directed_angle_eq_mod_pi P05 P04 P03 P02 P01 P00)
    (h04 : midpoint P08 P17 P26)
    : equal_length P07 P01 P01 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1179
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1179

theorem v06_sealed_holdout_1180
    (P00 P03 P05 P06 P07 P09 P12 P13 P15 P16 P18 P19 P23 P26 P30 : Point)
    (L10 L18 : Line)
    (C02 C16 : Circle)
    (h00 : length_sum P12 P18 P30 P09 P16 P23)
    (h01 : area_le P06 P19 P00 P13 P26 P07)
    (h02 : line_circle_intersection P19 L10 C16)
    (h03 : line_circle_intersection P03 L18 C02)
    (h04 : midpoint P15 P26 P05)
    : length_sum P30 P09 P12 P18 P16 P23 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1180
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1180

theorem v06_sealed_holdout_1181
    (P02 P03 P05 P09 P15 P16 P19 P22 P25 P27 P28 P29 P31 : Point)
    (L00 : Line)
    (h00 : equal_length P09 P29 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : angle_bisector_line P19 P03 P16 P27 L00)
    (h03 : directed_angle_eq_mod_pi P19 P22 P25 P28 P31 P02)
    (h04 : midpoint P22 P03 P16)
    : equal_length P09 P29 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1181
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1181

theorem v06_sealed_holdout_1182
    (P00 P02 P03 P04 P12 P13 P19 P22 P23 P24 P26 P30 P31 : Point)
    (L26 : Line)
    (C02 C04 C06 : Circle)
    (h00 : area_eq P30 P00 P22 P02 P12 P23)
    (h01 : area_eq P02 P12 P23 P03 P13 P24)
    (h02 : line_circle_intersection P19 L26 C04)
    (h03 : between P26 P31 P04)
    (h04 : circle_circle_intersection P19 C06 C02)
    : area_eq P30 P00 P22 P03 P13 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1182
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1182

theorem v06_sealed_holdout_1183
    (P04 P05 P06 P08 P11 P15 P16 P18 P19 P21 P23 P24 P25 P27 P29 P30 : Point)
    (C02 C22 : Circle)
    (h00 : equal_length P11 P29 P16 P27)
    (h01 : equal_length P16 P27 P05 P15)
    (h02 : directed_angle_eq_mod_pi P30 P27 P24 P21 P18 P15)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : directed_angle_eq_mod_pi P04 P21 P06 P23 P08 P25)
    : equal_length P11 P29 P05 P15 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1183
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1183

theorem v06_sealed_holdout_1184
    (P01 P02 P03 P04 P05 P10 P11 P14 P17 P23 P25 P27 P28 P30 : Point)
    (L00 L02 L08 : Line)
    (C14 : Circle)
    (h00 : angle_bisector_line P01 P14 P25 P03 L08)
    (h01 : midpoint P05 P04 P03)
    (h02 : angle_bisector_line P27 P02 P17 P28 L00)
    (h03 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h04 : line_circle_intersection P03 L02 C14)
    : angle_bisector P01 P14 P25 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1184
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1184

theorem v06_sealed_holdout_1185
    (P00 P03 P05 P06 P15 P16 P18 P24 P26 P27 P29 : Point)
    (L02 L06 L20 : Line)
    (C06 C18 C19 : Circle)
    (h00 : angle_bisector_line P29 P15 P24 P03 L06)
    (h01 : angle_bisector_line P18 P00 P16 P27 L20)
    (h02 : circle_circle_intersection P03 C18 C19)
    (h03 : directed_angle_eq_mod_pi P15 P26 P05 P16 P27 P06)
    (h04 : line_circle_intersection P03 L02 C06)
    : angle_bisector P29 P15 P24 P03 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1185
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1185

theorem v06_sealed_holdout_1186
    (P03 P04 P06 P07 P15 P16 P19 P22 P23 P24 P25 P31 : Point)
    (L02 : Line)
    (C02 C22 C30 : Circle)
    (h00 : directed_angle_eq_mod_pi P06 P22 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : midpoint P19 P22 P25)
    (h03 : line_circle_intersection P03 L02 C30)
    (h04 : circle_circle_intersection P19 C22 C02)
    : directed_angle_eq_mod_pi P06 P22 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1186
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1186

theorem v06_sealed_holdout_1187
    (P02 P03 P04 P07 P10 P12 P16 P21 P25 P26 P27 P29 P30 P31 : Point)
    (L18 : Line)
    (C26 : Circle)
    (h00 : directed_angle_eq_mod_2pi P27 P26 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : midpoint P26 P31 P04)
    (h03 : between P29 P12 P27)
    (h04 : line_circle_intersection P03 L18 C26)
    : directed_angle_eq_mod_2pi P27 P26 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1187
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1187

theorem v06_sealed_holdout_1188
    (P01 P02 P03 P04 P07 P08 P15 P16 P22 P23 P24 P29 P31 : Point)
    (C18 C19 : Circle)
    (h00 : directed_angle_eq_mod_pi P08 P22 P04 P15 P23 P31)
    (h01 : directed_angle_eq_mod_pi P15 P23 P31 P07 P16 P24)
    (h02 : area_le P01 P08 P15 P22 P29 P04)
    (h03 : circle_circle_intersection P03 C18 C19)
    (h04 : between P07 P02 P29)
    : directed_angle_eq_mod_pi P08 P22 P04 P07 P16 P24 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1188
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1188

theorem v06_sealed_holdout_1189
    (P02 P03 P04 P07 P10 P11 P16 P17 P21 P23 P25 P26 P27 P28 P29 P30 : Point)
    (L00 L02 : Line)
    (C14 : Circle)
    (h00 : directed_angle_eq_mod_2pi P29 P26 P10 P21 P30 P07)
    (h01 : directed_angle_eq_mod_2pi P21 P30 P07 P16 P25 P02)
    (h02 : angle_bisector_line P27 P03 P16 P28 L00)
    (h03 : directed_angle_eq_mod_pi P11 P30 P17 P04 P23 P10)
    (h04 : line_circle_intersection P03 L02 C14)
    : directed_angle_eq_mod_2pi P29 P26 P10 P16 P25 P02 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1189
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1189

theorem v06_sealed_holdout_1190
    (P05 P06 P07 P10 P12 P13 P14 P15 P16 P17 P18 P26 P27 P28 : Point)
    (L04 : Line)
    (C25 : Circle)
    (h00 : circle_through_three_noncollinear_points P18 P05 P16 C25)
    (h01 : between P12 P13 P14)
    (h02 : midpoint P15 P26 P05)
    (h03 : directed_angle_eq_mod_pi P18 P07 P28 P17 P06 P27)
    (h04 : angle_bisector_line P06 P10 P17 P28 L04)
    : triangle_pred P18 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1190
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1190

theorem v06_sealed_holdout_1191
    (P03 P04 P06 P07 P10 P16 P19 P22 P23 P29 : Point)
    (C02 C18 C19 C22 C30 : Circle)
    (h00 : equilateral P07 P04 P06)
    (h01 : circle_circle_intersection P19 C30 C02)
    (h02 : area_le P22 P03 P16 P29 P10 P23)
    (h03 : circle_circle_intersection P19 C22 C02)
    (h04 : circle_circle_intersection P03 C18 C19)
    : triangle_pred P07 P04 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1191
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1191

theorem v06_sealed_holdout_1192
    (P00 P04 P05 P08 P09 P10 P12 P14 P16 P17 P18 P19 P20 P25 P26 P27 P28 P29 P31 : Point)
    (L28 : Line)
    (C07 : Circle)
    (h00 : circle_through_three_noncollinear_points P20 P05 P16 C07)
    (h01 : directed_angle_eq_mod_pi P26 P31 P04 P09 P14 P19)
    (h02 : area_le P29 P12 P27 P10 P25 P08)
    (h03 : midpoint P00 P25 P18)
    (h04 : angle_bisector_line P08 P10 P17 P28 L28)
    : triangle_pred P20 P05 P16 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1192
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1192

theorem v06_sealed_holdout_1193
    (P00 P02 P03 P05 P06 P07 P09 P10 P14 P16 P17 P19 P24 P26 P27 P28 P29 : Point)
    (L08 L18 L20 : Line)
    (C18 : Circle)
    (h00 : equilateral P09 P05 P06)
    (h01 : angle_bisector_line P26 P00 P16 P27 L20)
    (h02 : line_circle_intersection P03 L18 C18)
    (h03 : area_le P07 P02 P29 P24 P19 P14)
    (h04 : angle_bisector_line P09 P10 P17 P28 L08)
    : triangle_pred P09 P05 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1193
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1193

theorem v06_sealed_holdout_1194
    (P03 P05 P06 P08 P10 P13 P17 P19 P20 P24 P26 P31 : Point)
    (C02 C18 C26 C30 : Circle)
    (h00 : equilateral P10 P05 P06)
    (h01 : between P08 P17 P26)
    (h02 : circle_circle_intersection P19 C30 C02)
    (h03 : circle_circle_intersection P03 C26 C18)
    (h04 : area_le P17 P24 P31 P06 P13 P20)
    : triangle_pred P10 P05 P06 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1194
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1194

theorem v06_sealed_holdout_1195
    (P00 P01 P03 P04 P08 P15 P19 P20 P22 P29 P31 : Point)
    (C18 C19 : Circle)
    (h00 : P19 = P08)
    (h01 : P01 = P20)
    (h02 : P00 = P31)
    (h03 : directed_angle_eq_mod_pi P01 P08 P15 P22 P29 P04)
    (h04 : circle_circle_intersection P03 C18 C19)
    : rotation_preserves_collinear P19 P01 P00 P08 P20 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1195
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1195

theorem v06_sealed_holdout_1196
    (P00 P01 P02 P03 P04 P05 P08 P15 P17 P19 P26 P31 : Point)
    (h00 : P15 = P08)
    (h01 : P02 = P19)
    (h02 : P31 = P00)
    (h03 : area_le P05 P04 P03 P02 P01 P00)
    (h04 : between P08 P17 P26)
    : rotation_preserves_collinear P15 P02 P31 P08 P19 P00 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1196
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1196

theorem v06_sealed_holdout_1197
    (P00 P03 P08 P09 P11 P12 P13 P14 P15 P16 P17 P19 P23 P30 P31 : Point)
    (h00 : P11 = P08)
    (h01 : P03 = P19)
    (h02 : P30 = P31)
    (h03 : midpoint P09 P00 P23)
    (h04 : area_le P12 P13 P14 P15 P16 P17)
    : rotation_preserves_collinear P11 P03 P30 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1197
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1197

theorem v06_sealed_holdout_1198
    (P03 P04 P07 P08 P09 P11 P13 P19 P24 P26 P28 P29 P31 : Point)
    (C02 C18 : Circle)
    (h00 : P07 = P08)
    (h01 : P04 = P19)
    (h02 : P29 = P31)
    (h03 : area_le P13 P28 P11 P26 P09 P24)
    (h04 : circle_circle_intersection P03 C02 C18)
    : rotation_preserves_collinear P07 P04 P29 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1198
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1198

theorem v06_sealed_holdout_1199
    (P03 P05 P07 P08 P09 P17 P19 P20 P22 P24 P28 P31 : Point)
    (h00 : P03 = P08)
    (h01 : P05 = P19)
    (h02 : P28 = P31)
    (h03 : between P17 P24 P31)
    (h04 : directed_angle_eq_mod_pi P20 P05 P22 P07 P24 P09)
    : rotation_preserves_collinear P03 P05 P28 P08 P19 P31 := by
  -- MARP_PROOF_REGION_START:v06_sealed_holdout_1199
  sorry
  -- MARP_PROOF_REGION_END:v06_sealed_holdout_1199

end MathAutoResearch.GeometryFull2D
