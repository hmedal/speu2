\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  cum_prob_j_2_k_0_s_0 + cum_prob_j_2_k_0_s_1 + cum_prob_j_2_k_0_s_2
   + cum_prob_j_2_k_0_s_3 + cum_prob_j_2_k_0_s_4 + cum_prob_j_2_k_0_s_5
   + cum_prob_j_2_k_0_s_6 + cum_prob_j_2_k_0_s_7 + cum_prob_j_2_k_1_s_0
   + cum_prob_j_2_k_1_s_1 + cum_prob_j_2_k_1_s_2 + cum_prob_j_2_k_1_s_3
   + cum_prob_j_2_k_1_s_4 + cum_prob_j_2_k_1_s_5 + cum_prob_j_2_k_1_s_6
   + cum_prob_j_2_k_1_s_7 + cum_prob_j_2_k_2_s_0 + cum_prob_j_2_k_2_s_1
   + cum_prob_j_2_k_2_s_2 + cum_prob_j_2_k_2_s_3 + cum_prob_j_2_k_2_s_4
   + cum_prob_j_2_k_2_s_5 + cum_prob_j_2_k_2_s_6 + cum_prob_j_2_k_2_s_7
Subject To
 first_component_s_0_k_0: - 368.9995457101158 allocVar_j_0_k_0
   + cum_prob_j_0_k_0_s_0 = 0
 first_component_s_0_k_1: - 155.9575586635308 allocVar_j_0_k_1
   + cum_prob_j_0_k_1_s_0 = 0
 first_component_s_0_k_2: - 67.71267827392209 allocVar_j_0_k_2
   + cum_prob_j_0_k_2_s_0 = 0
 first_component_s_1_k_0: - 2184.781521599794 allocVar_j_0_k_0
   + cum_prob_j_0_k_0_s_1 = 0
 first_component_s_1_k_1: - 923.397321983633 allocVar_j_0_k_1
   + cum_prob_j_0_k_1_s_1 = 0
 first_component_s_1_k_2: - 400.9148791394874 allocVar_j_0_k_2
   + cum_prob_j_0_k_2_s_1 = 0
 first_component_s_2_k_0: - 2137.464357663524 allocVar_j_0_k_0
   + cum_prob_j_0_k_0_s_2 = 0
 first_component_s_2_k_1: - 903.3987353832581 allocVar_j_0_k_1
   + cum_prob_j_0_k_1_s_2 = 0
 first_component_s_2_k_2: - 392.2320177763786 allocVar_j_0_k_2
   + cum_prob_j_0_k_2_s_2 = 0
 first_component_s_3_k_0: - 3637.022959700613 allocVar_j_0_k_0
   + cum_prob_j_0_k_0_s_3 = 0
 first_component_s_3_k_1: - 1537.186774868615 allocVar_j_0_k_1
   + cum_prob_j_0_k_1_s_3 = 0
 first_component_s_3_k_2: - 667.4061483494237 allocVar_j_0_k_2
   + cum_prob_j_0_k_2_s_3 = 0
 first_component_s_4_k_0: cum_prob_j_0_k_0_s_4 = 0
 first_component_s_4_k_1: - 1418.444799529068 allocVar_j_0_k_1
   + cum_prob_j_0_k_1_s_4 = 0
 first_component_s_4_k_2: - 2005.983872971595 allocVar_j_0_k_2
   + cum_prob_j_0_k_2_s_4 = 0
 first_component_s_5_k_0: cum_prob_j_0_k_0_s_5 = 0
 first_component_s_5_k_1: - 2270.761463554503 allocVar_j_0_k_1
   + cum_prob_j_0_k_1_s_5 = 0
 first_component_s_5_k_2: - 3211.341658672958 allocVar_j_0_k_2
   + cum_prob_j_0_k_2_s_5 = 0
 first_component_s_6_k_0: cum_prob_j_0_k_0_s_6 = 0
 first_component_s_6_k_1: - 2273.559950688024 allocVar_j_0_k_1
   + cum_prob_j_0_k_1_s_6 = 0
 first_component_s_6_k_2: - 3215.299317131309 allocVar_j_0_k_2
   + cum_prob_j_0_k_2_s_6 = 0
 first_component_s_7_k_0: cum_prob_j_0_k_0_s_7 = 0
 first_component_s_7_k_1: - 2835.667957804186 allocVar_j_0_k_1
   + cum_prob_j_0_k_1_s_7 = 0
 first_component_s_7_k_2: - 4010.240084313497 allocVar_j_0_k_2
   + cum_prob_j_0_k_2_s_7 = 0
 prob_chain_j_1_s_0: cum_prob_j_0_k_0_s_0 + cum_prob_j_0_k_1_s_0
   + cum_prob_j_0_k_2_s_0 - cum_prob_j_1_k_0_s_0
   - 2.366025403784438 cum_prob_j_1_k_1_s_0
   - 5.449489742783178 cum_prob_j_1_k_2_s_0 = 0
 prob_chain_j_2_s_0: cum_prob_j_1_k_0_s_0 + cum_prob_j_1_k_1_s_0
   + cum_prob_j_1_k_2_s_0 - cum_prob_j_2_k_0_s_0
   - 2.366025403784438 cum_prob_j_2_k_1_s_0
   - 5.449489742783178 cum_prob_j_2_k_2_s_0 = 0
 prob_chain_j_1_s_1: cum_prob_j_0_k_0_s_1 + cum_prob_j_0_k_1_s_1
   + cum_prob_j_0_k_2_s_1 - cum_prob_j_1_k_0_s_1
   - 2.366025403784438 cum_prob_j_1_k_1_s_1
   - 5.449489742783178 cum_prob_j_1_k_2_s_1 = 0
 prob_chain_j_2_s_1: cum_prob_j_1_k_0_s_1 + cum_prob_j_1_k_1_s_1
   + cum_prob_j_1_k_2_s_1 - 1e+07 cum_prob_j_2_k_0_s_1
   - 1.732050807568877 cum_prob_j_2_k_1_s_1
   - 1.224744871391589 cum_prob_j_2_k_2_s_1 = 0
 prob_chain_j_1_s_2: cum_prob_j_0_k_0_s_2 + cum_prob_j_0_k_1_s_2
   + cum_prob_j_0_k_2_s_2 - 1e+07 cum_prob_j_1_k_0_s_2
   - 1.732050807568877 cum_prob_j_1_k_1_s_2
   - 1.224744871391589 cum_prob_j_1_k_2_s_2 = 0
 prob_chain_j_2_s_2: cum_prob_j_1_k_0_s_2 + cum_prob_j_1_k_1_s_2
   + cum_prob_j_1_k_2_s_2 - cum_prob_j_2_k_0_s_2
   - 2.366025403784438 cum_prob_j_2_k_1_s_2
   - 5.449489742783178 cum_prob_j_2_k_2_s_2 = 0
 prob_chain_j_1_s_3: cum_prob_j_0_k_0_s_3 + cum_prob_j_0_k_1_s_3
   + cum_prob_j_0_k_2_s_3 - 1e+07 cum_prob_j_1_k_0_s_3
   - 1.732050807568877 cum_prob_j_1_k_1_s_3
   - 1.224744871391589 cum_prob_j_1_k_2_s_3 = 0
 prob_chain_j_2_s_3: cum_prob_j_1_k_0_s_3 + cum_prob_j_1_k_1_s_3
   + cum_prob_j_1_k_2_s_3 - 1e+07 cum_prob_j_2_k_0_s_3
   - 1.732050807568877 cum_prob_j_2_k_1_s_3
   - 1.224744871391589 cum_prob_j_2_k_2_s_3 = 0
 prob_chain_j_1_s_4: cum_prob_j_0_k_0_s_4 + cum_prob_j_0_k_1_s_4
   + cum_prob_j_0_k_2_s_4 - cum_prob_j_1_k_0_s_4
   - 2.366025403784438 cum_prob_j_1_k_1_s_4
   - 5.449489742783178 cum_prob_j_1_k_2_s_4 = 0
 prob_chain_j_2_s_4: cum_prob_j_1_k_0_s_4 + cum_prob_j_1_k_1_s_4
   + cum_prob_j_1_k_2_s_4 - cum_prob_j_2_k_0_s_4
   - 2.366025403784438 cum_prob_j_2_k_1_s_4
   - 5.449489742783178 cum_prob_j_2_k_2_s_4 = 0
 prob_chain_j_1_s_5: cum_prob_j_0_k_0_s_5 + cum_prob_j_0_k_1_s_5
   + cum_prob_j_0_k_2_s_5 - cum_prob_j_1_k_0_s_5
   - 2.366025403784438 cum_prob_j_1_k_1_s_5
   - 5.449489742783178 cum_prob_j_1_k_2_s_5 = 0
 prob_chain_j_2_s_5: cum_prob_j_1_k_0_s_5 + cum_prob_j_1_k_1_s_5
   + cum_prob_j_1_k_2_s_5 - 1e+07 cum_prob_j_2_k_0_s_5
   - 1.732050807568877 cum_prob_j_2_k_1_s_5
   - 1.224744871391589 cum_prob_j_2_k_2_s_5 = 0
 prob_chain_j_1_s_6: cum_prob_j_0_k_0_s_6 + cum_prob_j_0_k_1_s_6
   + cum_prob_j_0_k_2_s_6 - 1e+07 cum_prob_j_1_k_0_s_6
   - 1.732050807568877 cum_prob_j_1_k_1_s_6
   - 1.224744871391589 cum_prob_j_1_k_2_s_6 = 0
 prob_chain_j_2_s_6: cum_prob_j_1_k_0_s_6 + cum_prob_j_1_k_1_s_6
   + cum_prob_j_1_k_2_s_6 - cum_prob_j_2_k_0_s_6
   - 2.366025403784438 cum_prob_j_2_k_1_s_6
   - 5.449489742783178 cum_prob_j_2_k_2_s_6 = 0
 prob_chain_j_1_s_7: cum_prob_j_0_k_0_s_7 + cum_prob_j_0_k_1_s_7
   + cum_prob_j_0_k_2_s_7 - 1e+07 cum_prob_j_1_k_0_s_7
   - 1.732050807568877 cum_prob_j_1_k_1_s_7
   - 1.224744871391589 cum_prob_j_1_k_2_s_7 = 0
 prob_chain_j_2_s_7: cum_prob_j_1_k_0_s_7 + cum_prob_j_1_k_1_s_7
   + cum_prob_j_1_k_2_s_7 - 1e+07 cum_prob_j_2_k_0_s_7
   - 1.732050807568877 cum_prob_j_2_k_1_s_7
   - 1.224744871391589 cum_prob_j_2_k_2_s_7 = 0
 VUB_j_0_k_0_s_0: - 368.9995457101158 allocVar_j_0_k_0
   + cum_prob_j_0_k_0_s_0 <= 0
 VUB_j_0_k_1_s_0: - 368.9995457101158 allocVar_j_0_k_1
   + cum_prob_j_0_k_1_s_0 <= 0
 VUB_j_0_k_2_s_0: - 368.9995457101158 allocVar_j_0_k_2
   + cum_prob_j_0_k_2_s_0 <= 0
 VUB_j_1_k_0_s_0: - 368.9995457101158 allocVar_j_1_k_0
   + cum_prob_j_1_k_0_s_0 <= 0
 VUB_j_1_k_1_s_0: - 368.9995457101158 allocVar_j_1_k_1
   + cum_prob_j_1_k_1_s_0 <= 0
 VUB_j_1_k_2_s_0: - 368.9995457101158 allocVar_j_1_k_2
   + cum_prob_j_1_k_2_s_0 <= 0
 VUB_j_2_k_0_s_0: - 368.9995457101158 allocVar_j_2_k_0
   + cum_prob_j_2_k_0_s_0 <= 0
 VUB_j_2_k_1_s_0: - 368.9995457101158 allocVar_j_2_k_1
   + cum_prob_j_2_k_1_s_0 <= 0
 VUB_j_2_k_2_s_0: - 368.9995457101158 allocVar_j_2_k_2
   + cum_prob_j_2_k_2_s_0 <= 0
 VUB_j_0_k_0_s_1: - 2184.781521599794 allocVar_j_0_k_0
   + cum_prob_j_0_k_0_s_1 <= 0
 VUB_j_0_k_1_s_1: - 2184.781521599794 allocVar_j_0_k_1
   + cum_prob_j_0_k_1_s_1 <= 0
 VUB_j_0_k_2_s_1: - 2184.781521599794 allocVar_j_0_k_2
   + cum_prob_j_0_k_2_s_1 <= 0
 VUB_j_1_k_0_s_1: - 2184.781521599794 allocVar_j_1_k_0
   + cum_prob_j_1_k_0_s_1 <= 0
 VUB_j_1_k_1_s_1: - 2184.781521599794 allocVar_j_1_k_1
   + cum_prob_j_1_k_1_s_1 <= 0
 VUB_j_1_k_2_s_1: - 2184.781521599794 allocVar_j_1_k_2
   + cum_prob_j_1_k_2_s_1 <= 0
 VUB_j_2_k_0_s_1: - 2184.781521599794 allocVar_j_2_k_0
   + cum_prob_j_2_k_0_s_1 <= 0
 VUB_j_2_k_1_s_1: - 2184.781521599794 allocVar_j_2_k_1
   + cum_prob_j_2_k_1_s_1 <= 0
 VUB_j_2_k_2_s_1: - 2184.781521599794 allocVar_j_2_k_2
   + cum_prob_j_2_k_2_s_1 <= 0
 VUB_j_0_k_0_s_2: - 2137.464357663524 allocVar_j_0_k_0
   + cum_prob_j_0_k_0_s_2 <= 0
 VUB_j_0_k_1_s_2: - 2137.464357663524 allocVar_j_0_k_1
   + cum_prob_j_0_k_1_s_2 <= 0
 VUB_j_0_k_2_s_2: - 2137.464357663524 allocVar_j_0_k_2
   + cum_prob_j_0_k_2_s_2 <= 0
 VUB_j_1_k_0_s_2: - 2137.464357663524 allocVar_j_1_k_0
   + cum_prob_j_1_k_0_s_2 <= 0
 VUB_j_1_k_1_s_2: - 2137.464357663524 allocVar_j_1_k_1
   + cum_prob_j_1_k_1_s_2 <= 0
 VUB_j_1_k_2_s_2: - 2137.464357663524 allocVar_j_1_k_2
   + cum_prob_j_1_k_2_s_2 <= 0
 VUB_j_2_k_0_s_2: - 2137.464357663524 allocVar_j_2_k_0
   + cum_prob_j_2_k_0_s_2 <= 0
 VUB_j_2_k_1_s_2: - 2137.464357663524 allocVar_j_2_k_1
   + cum_prob_j_2_k_1_s_2 <= 0
 VUB_j_2_k_2_s_2: - 2137.464357663524 allocVar_j_2_k_2
   + cum_prob_j_2_k_2_s_2 <= 0
 VUB_j_0_k_0_s_3: - 3637.022959700613 allocVar_j_0_k_0
   + cum_prob_j_0_k_0_s_3 <= 0
 VUB_j_0_k_1_s_3: - 3637.022959700613 allocVar_j_0_k_1
   + cum_prob_j_0_k_1_s_3 <= 0
 VUB_j_0_k_2_s_3: - 3637.022959700613 allocVar_j_0_k_2
   + cum_prob_j_0_k_2_s_3 <= 0
 VUB_j_1_k_0_s_3: - 3637.022959700613 allocVar_j_1_k_0
   + cum_prob_j_1_k_0_s_3 <= 0
 VUB_j_1_k_1_s_3: - 3637.022959700613 allocVar_j_1_k_1
   + cum_prob_j_1_k_1_s_3 <= 0
 VUB_j_1_k_2_s_3: - 3637.022959700613 allocVar_j_1_k_2
   + cum_prob_j_1_k_2_s_3 <= 0
 VUB_j_2_k_0_s_3: - 3637.022959700613 allocVar_j_2_k_0
   + cum_prob_j_2_k_0_s_3 <= 0
 VUB_j_2_k_1_s_3: - 3637.022959700613 allocVar_j_2_k_1
   + cum_prob_j_2_k_1_s_3 <= 0
 VUB_j_2_k_2_s_3: - 3637.022959700613 allocVar_j_2_k_2
   + cum_prob_j_2_k_2_s_3 <= 0
 VUB_j_0_k_0_s_4: - 2456.818460516197 allocVar_j_0_k_0
   + cum_prob_j_0_k_0_s_4 <= 0
 VUB_j_0_k_1_s_4: - 2456.818460516197 allocVar_j_0_k_1
   + cum_prob_j_0_k_1_s_4 <= 0
 VUB_j_0_k_2_s_4: - 2456.818460516197 allocVar_j_0_k_2
   + cum_prob_j_0_k_2_s_4 <= 0
 VUB_j_1_k_0_s_4: - 2456.818460516197 allocVar_j_1_k_0
   + cum_prob_j_1_k_0_s_4 <= 0
 VUB_j_1_k_1_s_4: - 2456.818460516197 allocVar_j_1_k_1
   + cum_prob_j_1_k_1_s_4 <= 0
 VUB_j_1_k_2_s_4: - 2456.818460516197 allocVar_j_1_k_2
   + cum_prob_j_1_k_2_s_4 <= 0
 VUB_j_2_k_0_s_4: - 2456.818460516197 allocVar_j_2_k_0
   + cum_prob_j_2_k_0_s_4 <= 0
 VUB_j_2_k_1_s_4: - 2456.818460516197 allocVar_j_2_k_1
   + cum_prob_j_2_k_1_s_4 <= 0
 VUB_j_2_k_2_s_4: - 2456.818460516197 allocVar_j_2_k_2
   + cum_prob_j_2_k_2_s_4 <= 0
 VUB_j_0_k_0_s_5: - 3933.074226745864 allocVar_j_0_k_0
   + cum_prob_j_0_k_0_s_5 <= 0
 VUB_j_0_k_1_s_5: - 3933.074226745864 allocVar_j_0_k_1
   + cum_prob_j_0_k_1_s_5 <= 0
 VUB_j_0_k_2_s_5: - 3933.074226745864 allocVar_j_0_k_2
   + cum_prob_j_0_k_2_s_5 <= 0
 VUB_j_1_k_0_s_5: - 3933.074226745864 allocVar_j_1_k_0
   + cum_prob_j_1_k_0_s_5 <= 0
 VUB_j_1_k_1_s_5: - 3933.074226745864 allocVar_j_1_k_1
   + cum_prob_j_1_k_1_s_5 <= 0
 VUB_j_1_k_2_s_5: - 3933.074226745864 allocVar_j_1_k_2
   + cum_prob_j_1_k_2_s_5 <= 0
 VUB_j_2_k_0_s_5: - 3933.074226745864 allocVar_j_2_k_0
   + cum_prob_j_2_k_0_s_5 <= 0
 VUB_j_2_k_1_s_5: - 3933.074226745864 allocVar_j_2_k_1
   + cum_prob_j_2_k_1_s_5 <= 0
 VUB_j_2_k_2_s_5: - 3933.074226745864 allocVar_j_2_k_2
   + cum_prob_j_2_k_2_s_5 <= 0
 VUB_j_0_k_0_s_6: - 3937.92134864545 allocVar_j_0_k_0
   + cum_prob_j_0_k_0_s_6 <= 0
 VUB_j_0_k_1_s_6: - 3937.92134864545 allocVar_j_0_k_1
   + cum_prob_j_0_k_1_s_6 <= 0
 VUB_j_0_k_2_s_6: - 3937.92134864545 allocVar_j_0_k_2
   + cum_prob_j_0_k_2_s_6 <= 0
 VUB_j_1_k_0_s_6: - 3937.92134864545 allocVar_j_1_k_0
   + cum_prob_j_1_k_0_s_6 <= 0
 VUB_j_1_k_1_s_6: - 3937.92134864545 allocVar_j_1_k_1
   + cum_prob_j_1_k_1_s_6 <= 0
 VUB_j_1_k_2_s_6: - 3937.92134864545 allocVar_j_1_k_2
   + cum_prob_j_1_k_2_s_6 <= 0
 VUB_j_2_k_0_s_6: - 3937.92134864545 allocVar_j_2_k_0
   + cum_prob_j_2_k_0_s_6 <= 0
 VUB_j_2_k_1_s_6: - 3937.92134864545 allocVar_j_2_k_1
   + cum_prob_j_2_k_1_s_6 <= 0
 VUB_j_2_k_2_s_6: - 3937.92134864545 allocVar_j_2_k_2
   + cum_prob_j_2_k_2_s_6 <= 0
 VUB_j_0_k_0_s_7: - 4911.520976311929 allocVar_j_0_k_0
   + cum_prob_j_0_k_0_s_7 <= 0
 VUB_j_0_k_1_s_7: - 4911.520976311929 allocVar_j_0_k_1
   + cum_prob_j_0_k_1_s_7 <= 0
 VUB_j_0_k_2_s_7: - 4911.520976311929 allocVar_j_0_k_2
   + cum_prob_j_0_k_2_s_7 <= 0
 VUB_j_1_k_0_s_7: - 4911.520976311929 allocVar_j_1_k_0
   + cum_prob_j_1_k_0_s_7 <= 0
 VUB_j_1_k_1_s_7: - 4911.520976311929 allocVar_j_1_k_1
   + cum_prob_j_1_k_1_s_7 <= 0
 VUB_j_1_k_2_s_7: - 4911.520976311929 allocVar_j_1_k_2
   + cum_prob_j_1_k_2_s_7 <= 0
 VUB_j_2_k_0_s_7: - 4911.520976311929 allocVar_j_2_k_0
   + cum_prob_j_2_k_0_s_7 <= 0
 VUB_j_2_k_1_s_7: - 4911.520976311929 allocVar_j_2_k_1
   + cum_prob_j_2_k_1_s_7 <= 0
 VUB_j_2_k_2_s_7: - 4911.520976311929 allocVar_j_2_k_2
   + cum_prob_j_2_k_2_s_7 <= 0
 multiple_choic_j_0: allocVar_j_0_k_0 + allocVar_j_0_k_1 + allocVar_j_0_k_2
   = 1
 multiple_choic_j_1: allocVar_j_1_k_0 + allocVar_j_1_k_1 + allocVar_j_1_k_2
   = 1
 multiple_choic_j_2: allocVar_j_2_k_0 + allocVar_j_2_k_1 + allocVar_j_2_k_2
   = 1
 budget: allocVar_j_0_k_1 + 2 allocVar_j_0_k_2 + allocVar_j_1_k_1
   + 2 allocVar_j_1_k_2 + allocVar_j_2_k_1 + 2 allocVar_j_2_k_2 <= 1
Bounds
Binaries
 allocVar_j_0_k_0 allocVar_j_0_k_1 allocVar_j_0_k_2 allocVar_j_1_k_0
 allocVar_j_1_k_1 allocVar_j_1_k_2 allocVar_j_2_k_0 allocVar_j_2_k_1
 allocVar_j_2_k_2
End
