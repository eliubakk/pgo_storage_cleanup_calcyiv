import csv

import operator

ops = {
	'>': operator.gt,
	'<': operator.lt,
}

scans_by_name = {}
scans_by_GL_Evo = {}
scans_by_UL_Evo = {}
best_iv_scans = {}
best_LL_scans = {}
best_GL_scans = {}
best_UL_scans = {}

def filter_scans_by_field(scan_list, field, cast, compare_op):
	first_valid_idx = 0
	while first_valid_idx < len(scan_list) and scan_list[first_valid_idx][field] == ' - ':
		first_valid_idx += 1
	
	if first_valid_idx == len(scan_list):
		return []

	best = cast(scan_list[first_valid_idx][field])
	best_scans = [scan_list[first_valid_idx]]

	if first_valid_idx + 1 == len(scan_list):
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
	return best_scans

def main():
	with open('calcyiv_history.csv', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			scans_by_name.setdefault(row['Name'],[])
			scans_by_name[row['Name']].append(row)
			scans_by_GL_Evo.setdefault(row['GL Evo'],[])
			scans_by_GL_Evo[row['GL Evo']].append(row)
			scans_by_UL_Evo.setdefault(row['UL Evo'],[])
			scans_by_UL_Evo[row['UL Evo']].append(row)


		for (pokemon_name, scan_list) in scans_by_name.items():
			best_iv_scans[pokemon_name] = filter_scans_by_field(scan_list, 'max IV%', float, '>')
			print("*******************Best {} IV Scans:*******************\n".format(pokemon_name), best_iv_scans[pokemon_name], '\n')
			best_LL_scans[pokemon_name] = filter_scans_by_field(scan_list, 'LL Rank (max)', int, '<')
			print("*******************Best {} LL Scans:*******************\n".format(pokemon_name), best_LL_scans[pokemon_name], '\n')
		for (pokemon_name, scan_list) in scans_by_GL_Evo.items():
			best_GL_scans[pokemon_name] = filter_scans_by_field(scan_list, 'GL Rank (max)', int, '<')
			print("*******************Best {} GL Scans:*******************\n".format(pokemon_name), best_GL_scans[pokemon_name], '\n')
		for (pokemon_name, scan_list) in scans_by_UL_Evo.items():
			best_UL_scans[pokemon_name] = filter_scans_by_field(scan_list, 'UL Rank (max)', int, '<')
			print("*******************Best {} UL Scans:*******************\n".format(pokemon_name), best_UL_scans[pokemon_name], '\n')

if __name__ == '__main__':
	main()