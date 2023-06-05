import csv

import operator

ops = {
	'>': operator.gt,
	'<': operator.lt,
}

pokemon_w_gender_differences = [3,12,19,20,25,26,41,42,44,45,64,65,84,85,97,111,112,118,119,123,129,130,133,154,165,166,178,185,186,190,194,195,198,202,203,207,208,212,214,215,217,221,224,229,232,255,256,257,267,269,272,274,275,307,308,315,316,317,322,323,332,350,369,396,397,398,399,400,401,402,403,404,405,407,415,417,418,419,424,443,444,445,449,450,453,454,456,457,459,460,461,464,465,473,521,592,593,668,678,876]

scans_by_name_male = {}
scans_by_name_female = {}
scans_by_name = {}
scans_by_GL_Evo = {}
scans_by_UL_Evo = {}
shadow_scans_by_GL_Evo = {}
shadow_scans_by_UL_Evo = {}
best_iv_scans_male = {}
best_iv_scans_female = {}
best_iv_scans = {}
best_LL_scans = {}
best_shadow_GL_scans = {}
best_shadow_UL_scans = {}
best_non_shadow_GL_scans = {}
best_non_shadow_UL_scans = {}

def filter_scans_by_field(scan_list, field, cast, compare_op):
	first_valid_idx = 0
	while first_valid_idx < len(scan_list) and scan_list[first_valid_idx][field] == ' - ':
		first_valid_idx += 1
	
	if first_valid_idx == len(scan_list):
		return []

	best = cast(scan_list[first_valid_idx][field])
	best_scans = [scan_list[first_valid_idx]]

	if first_valid_idx + 1 == len(scan_list):
		# TODO: Fix overritting of box from max IV -> LL, UL, GL?
		best_scans[0]['Box'] = field
		return best_scans

	for scan in scan_list[first_valid_idx+1:]:
		if scan[field] == ' - ':
			continue

		scan_val = cast(scan[field])
		if ops[compare_op](scan_val, best):
			best = scan_val
			best_scans = [scan]
		elif scan_val == best:
			best_scans.append(scan)

	for scan in best_scans:
		# TODO: Fix overritting of box from max IV -> LL, UL, GL?
		scan['Box'] = field
	return best_scans

def main():
	with open('calcyiv_history.csv', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if int(row['Nr']) in pokemon_w_gender_differences:
				if row['Gender'] == '♂':
					scans_by_name_male.setdefault(row['Name'],[])
					scans_by_name_male[row['Name']].append(row)
				elif row['Gender'] == '♀':
					scans_by_name_female.setdefault(row['Name'], [])
					scans_by_name_female[row['Name']].append(row)
			else:
				scans_by_name.setdefault(row['Name'],[])
				scans_by_name[row['Name']].append(row)

			if 'Shadow' in row['Name']:
				shadow_scans_by_GL_Evo.setdefault(row['GL Evo'], [])
				shadow_scans_by_GL_Evo[row['GL Evo']].append(row)
				shadow_scans_by_UL_Evo.setdefault(row['UL Evo'], [])
				shadow_scans_by_UL_Evo[row['UL Evo']].append(row)
			else:
				scans_by_GL_Evo.setdefault(row['GL Evo'],[])
				scans_by_GL_Evo[row['GL Evo']].append(row)
				scans_by_UL_Evo.setdefault(row['UL Evo'],[])
				scans_by_UL_Evo[row['UL Evo']].append(row)

		for (pokemon_name, scan_list) in scans_by_name_male.items():
			best_iv_scans_male[pokemon_name] = filter_scans_by_field(scan_list, 'max IV%', float, '>')
			best_LL_scans[pokemon_name] = filter_scans_by_field(scan_list, 'LL Rank (max)', int, '<')
		for (pokemon_name, scan_list) in scans_by_name_female.items():
			best_iv_scans_female[pokemon_name] = filter_scans_by_field(scan_list, 'max IV%', float, '>')
			best_LL_scans[pokemon_name] = filter_scans_by_field(best_LL_scans.setdefault(pokemon_name,[]) + scan_list, 'LL Rank (max)', int, '<')
		for (pokemon_name, scan_list) in scans_by_name.items():
			best_iv_scans[pokemon_name] = filter_scans_by_field(scan_list, 'max IV%', float, '>')
			best_LL_scans[pokemon_name] = filter_scans_by_field(scan_list, 'LL Rank (max)', int, '<')
		for (pokemon_name, scan_list) in shadow_scans_by_GL_Evo.items():
			best_shadow_GL_scans[pokemon_name] = filter_scans_by_field(scan_list, 'GL Rank (max)', int, '<')
		for (pokemon_name, scan_list) in shadow_scans_by_UL_Evo.items():
			best_shadow_UL_scans[pokemon_name] = filter_scans_by_field(scan_list, 'UL Rank (max)', int, '<')
		for (pokemon_name, scan_list) in scans_by_GL_Evo.items():
			best_non_shadow_GL_scans[pokemon_name] = filter_scans_by_field(scan_list, 'GL Rank (max)', int, '<')
		for (pokemon_name, scan_list) in scans_by_UL_Evo.items():
			best_non_shadow_UL_scans[pokemon_name] = filter_scans_by_field(scan_list, 'UL Rank (max)', int, '<')

		for best_scans in (best_iv_scans_male, best_iv_scans_female, best_iv_scans, best_LL_scans, best_shadow_GL_scans, best_non_shadow_GL_scans, best_shadow_UL_scans, best_non_shadow_UL_scans):	
			for (pokemon_name, scan_list) in best_scans.items():
				if len(scan_list):
					print("*******************{0}{1}{2} Scans:*******************\n".format(pokemon_name, (lambda scan: f" {scan['Gender']} " if int(scan['Nr']) in pokemon_w_gender_differences else " ")(scan_list[0]), scan_list[0]['Box']), scan_list, '\n')

if __name__ == '__main__':
	main()