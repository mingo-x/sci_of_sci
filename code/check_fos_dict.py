dir_path = "/mnt/ds3lab/yanping/mag/data"
# read in fos_kdd
f_kdd = open(dir_path+"/FieldsOfStudy.txt","r")
fos_dict = {}
for line in f_kdd:
	fos_id = line[0:8]
	fos_name = line[9:-1]
	print(fos_id,fos_name)
	fos_dict[fos_id] = fos_name
f_kdd.close()

#check fos_mag
f_mag = open(dir_path+"/fos.txt","r")
no_count = 0
for line in f_mag:
	fos_name = line[:-1]
	if fos_name in fos_dict:
		print(fos_name, fos_dict[fos_name])
	else:
		print(fos_name,"no corresponding")
		no_count += 1
print("no corresponding",no_count)
f_mag.close()
