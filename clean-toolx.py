import logging, json, os, sys, platform, re
from os.path import getsize
try:
	def convert_size(size):
		try:
			if size >= 1000:
				if size >= 1000*1000:
					if size >= 1000*1000*1000:
						if size >= 1000*1000*1000*1000:
							total_size = str(format(size / (1000*1000*1000*1000), ".2f")) + "TB"
						else:
							total_size = str(format(size / (1000*1000*1000), ".2f")) + "GB"
					else:
						total_size = str(format(size / (1000*1000), ".2f")) + "MB"
				else:
					total_size = str(format(size / 1000, ".2f")) + "KB"
			else:
				total_size = str(format(size, ".2f")) + "B"
		except OSError:
			logging.error("索引失败!")
			input()
			sys.exit()
		return total_size
	logging.basicConfig(level = logging.DEBUG,format = '[PID #%(process)d] [%(levelname)s] %(message)s')
	logger = logging.getLogger(__name__)
	print()
	print("    #==================================#")
	print("    |   clean-toolx v1.1 By @延时qwq   |")
	print("    #==================================#")
	print()
	if os.listdir("./plugins"):
		clean_count = 0
		clean_size = 0
		total_size = 0
		total_count = 0
		plugin_count = 0
		for root,dirs,files in os.walk("./plugins"):
			for file in files:
				if os.path.splitext(file)[-1]=='.json':
					plugin_count += 1
		if plugin_count == 0:
			logging.error("未检测到任何插件!")
			sys.exit()
		else:
			logging.info("检测到" + str(plugin_count) + "个插件.")
		for root,dirs,files in os.walk("./plugins"):
			for file in files:
				if os.path.splitext(file)[-1] == ".json":
					plugin_data = open("./plugins/" + file).read()
				else:
					continue
				try:
					plugin_config = json.loads(plugin_data)
				except json.decoder.JSONDecodeError as e:
					logging.error("插件配置有误!请检查插件完整性(" + file + ").")
					continue
				logging.info("插件名称: " + plugin_config["name"] + " (" + file + ")")
				logging.info("插件作者: " + plugin_config["author"])
				logging.info("插件版本: " + plugin_config["version_name"])
				if plugin_config["platform"] != platform.system().lower():
					logging.warn("此插件不适配此操作系统!")
					continue
				print("")
				for rule in plugin_config["rules"]:
					logging.info("正在清理 " + rule["name"] + " ...")
					path_list = []
					try:
						for folders in rule["folders"]:
							path = folders["path"]
							match = re.findall('\$\{.+\}', path)
							if match != None:
								for varible in match:
									path = path.replace(varible, os.environ[varible[2: -1]])
							for root,dirs,names in os.walk(path):
								for filename in names:
									if os.path.splitext(os.path.join(root,filename))[-1].lower() == folders["extension"].lower() or folders["extension"] == "*":
										path_list.append(os.path.join(root,filename))
										total_size = total_size + getsize(os.path.join(root,filename))
						for file in rule["files"]:
							path_list.append(os.path.join(root,filename))
							total_size = total_size + getsize(os.path.join(root,filename))
					except:
						pass
					file_count = len(path_list)
					if file_count == 0:
						logging.info("未检测到文件.\n")
						continue
					print("")
					logging.info("检测到" + str(file_count) + "个文件(" + convert_size(total_size) + "):")
					total_count = total_count + file_count
					count = 0
					for file_path in path_list:
						try:
							print("\t [" + convert_size(getsize(file_path)) + "]\t" + file_path)
							count = count + 1
						except FileNotFoundError:
							del path_list[file_path]
						if count >= 10:
							print("\t  ......\t ......")
							break
					print("")
					if rule["warning_level"] == 0:
						pass
					elif rule["warning_level"] == 1:
						input("[PID " + str(str(os.getpid())) + "] [INFO] 按[Enter]开始清理...")
					elif rule["warning_level"] == 2:
						while True:
							answer = input("[PID #" + str(os.getpid()) + "] [WARN] 这条规则可能会影响您的正常使用,确定继续吗?[Y/n]")
							if answer.upper() == "N":
								break
							elif answer.upper() == "Y":
								logging.info("忽略警告.")
								break
							else:
								continue
						if answer.upper() == "N":
							continue
					elif rule["warning_level"] == 3:
						while True:
							answer = input("[PID #" + str(os.getpid()) + "] [WARN] 这条规则会影响您的正常使用,确定继续吗?[y/N]")
							if answer.upper() == "N":
								break
							elif answer.upper() == "Y":
								logging.info("忽略警告.")
								break
							else:
								continue
						if answer.upper() == "N":
							continue
					elif rule["warning_level"] == 4:
						while True:
							answer = input("[PID #" + str(os.getpid()) + "] [WARN] 这条规则可能会损坏/删除您的数据,确定继续吗?[y/N]")
							if answer.upper() == "N":
								break
							elif answer.upper() == "Y":
								logging.info("忽略警告.")
								break
							else:
								continue
						if answer.upper() == "N":
							continue
					elif rule["warning_level"] == 5:
						while True:
							answer = input("[PID #" + str(os.getpid()) + "] [WARN] 这条规则会损坏/删除您的重要数据,确定继续吗?[y/N]")
							if answer.upper() == "N":
								break
							elif answer.upper() == "Y":
								logging.info("忽略警告.")
								break
							else:
								continue
						if answer.upper() == "N":
							continue
					logging.info("正在清理文件...")
					count = 1
					for file in path_list:
						try:
							filesize = getsize(file)
							os.remove(file)
						except PermissionError as e:
							if "[WinError 5]" in str(e):
								print("\t [" + str(count) + "/" + str(file_count) + "] \t拒绝访问 - " + file)
							if "[WinError 32]" in str(e):
								print("\t [" + str(count) + "/" + str(file_count) + "] \t拒绝访问 - " + file)
						else:
							print("\t [" + str(count) + "/" + str(file_count) + "] \t删除文件 - " + file)
							clean_size = clean_size + filesize
							clean_count = clean_count + 1
						count = count + 1
					print("")
				print("")
			print("")
			logging.info("清理完毕!")
			try:
				logging.info("清理了" + str(clean_count) + "个文件(" + convert_size(clean_size) + ").")
				if total_count - clean_count > 0:
					logging.info("有" + str(total_count - clean_count) + "个文件(" + convert_size(total_size - clean_size) + ")无法清理.")
			except NameError:
				logging.info("未清理文件.")
	else:
		logging.error("未检测到任何插件!")
		sys.exit()
except BaseException as e:
	if isinstance(e, KeyboardInterrupt):
		logging.error("进程终止!")