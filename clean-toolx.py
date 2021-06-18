import logging, json, os, sys, platform, re, time
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
	logging.basicConfig(level = logging.INFO,format = '[PID #%(process)d] [%(levelname)s] %(message)s')
	logger = logging.getLogger(__name__)
	logging.info("")
	logging.info("	#==================================#")
	logging.info("	|   clean-toolx v1.1.4 By @延时qwq   |")
	logging.info("	#==================================#")
	logging.info("")
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
			print("\n")
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
					logging.error("错误信息: " + str(e))
					print()
					continue
				logging.info("插件名称: " + plugin_config["name"] + " (" + file + ")")
				logging.info("插件作者: " + plugin_config["author"])
				logging.info("插件版本: " + plugin_config["version_name"])
				if plugin_config["platform"] != platform.system().lower():
					logging.warn("此插件不适配此操作系统!")
					continue
				for rule in plugin_config["rules"]:
					rule_size = 0
					logging.info("")
					logging.info("正在索引 " + rule["name"] + " ...")
					path_list = []
					if "paths" in rule:
						for paths in rule["paths"]:
							path = paths["path"]
							scan = paths["scan_path"]
							if "depth" in paths:
								depth = paths["depth"]
							else:
								depth = 1919810
							if "excludes" in paths:
								excludes = []
								for exclude in paths["excludes"]:
									match = re.findall('\$\{.+?\}', exclude)
									if match != None:
										for varible in match:
											excludes.append(exclude.replace(varible, os.environ[varible[2: -1]]))
							else:
								excludes = []
							match = re.findall('\$\{.+?\}', scan)
							if match != None:
								for varible in match:
									scan = scan.replace(varible, os.environ[varible[2: -1]])
							logging.info("正在扫描 " + scan + " ...")
							match = re.findall('\$\{.+?\}', path)
							if match != None:
								for varible in match:
									path = path.replace(varible, os.environ[varible[2: -1]])
							depth_count = 1
							for root,dirs,names in os.walk(scan):
								continue_signal = False
								if depth_count == depth:
									break
								logging.debug("root = " + root)
								for exclude in excludes:
									logging.debug("exclude = " + exclude)
									match = re.match(exclude.replace("\\","\\\\"), root)
									if match != None:
										continue_signal = True
										break
								if continue_signal == True:
									continue
								for filename in names:
									match = re.match(path.replace("\\","\\\\"), os.path.join(root,filename))
									if match != None:
										try:
											getsize(os.path.join(root,filename))
										except FileNotFoundError as e:
											continue
										path_list.append(os.path.join(root,filename))
										total_size = total_size + getsize(os.path.join(root,filename))
										rule_size = rule_size + getsize(os.path.join(root,filename))
								depth_count += 1
					else:
						logging.error("插件配置有误!请检查插件完整性(" + file + ").")
					file_count = len(path_list)
					if file_count == 0:
						logging.info("未检测到文件.")
						continue
					logging.info("")
					logging.info("检测到" + str(file_count) + "个文件(" + convert_size(rule_size) + "):")
					total_count = total_count + file_count
					count = 0
					for file_path in path_list:
						try:
							filesize = convert_size(getsize(file_path))
							logging.info("\t [" + filesize + "]\t" + file_path)
							count = count + 1
						except FileNotFoundError:
							path_list.remove(file_path)
						if count >= 10:
							logging.info("\t  ......\t ......")
							break
					logging.info("")
					if rule["warning_level"] == 0:
						pass
					elif rule["warning_level"] == 1:
						input("[PID #" + str(str(os.getpid())) + "] [INFO] 按[Enter]开始清理...")
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
								logging.info("\t [" + str(count) + "/" + str(file_count) + "] \t拒绝访问 - " + file)
							if "[WinError 32]" in str(e):
								logging.info("\t [" + str(count) + "/" + str(file_count) + "] \t拒绝访问 - " + file)
						else:
							logging.info("\t [" + str(count) + "/" + str(file_count) + "] \t删除文件 - " + file)
							clean_size = clean_size + filesize
							clean_count = clean_count + 1
						count = count + 1
				print("")
			print("")
			logging.info("清理完毕!")
			try:
				logging.info("清理了" + str(clean_count) + "个文件(" + convert_size(clean_size) + ").")
				if total_count - clean_count > 0:
					logging.info("有" + str(total_count - clean_count) + "个文件(" + convert_size(total_size - clean_size) + ")未清理.")
			except NameError:
				logging.info("未清理文件.")
	else:
		logging.error("未检测到任何插件!")
		sys.exit()
except BaseException as e:
	logging.error(e)
	if isinstance(e, KeyboardInterrupt):
		logging.info("")
		logging.error("进程终止!")
except SystemExit as e:
	logging.info("退出程序!")