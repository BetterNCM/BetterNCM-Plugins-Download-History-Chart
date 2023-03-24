import git
import json

repo_path = './BetterNCM-PluginMarket-Analyze'
repo_url = 'https://github.com/BetterNCM/BetterNCM-PluginMarket-Analyze'
file_path = 'downloads.json'

try:
	repo = git.Repo(repo_path)
	print('Pulling latest changes...')
	repo.remotes.origin.pull()

except git.exc.NoSuchPathError:
	print('Cloning repository...')
	git.Repo.clone_from(repo_url, repo_path)
	repo = git.Repo(repo_path)


file_obj = repo.heads.main.commit.tree[file_path]

cnt = 0

data = []
slugs = []
last_download = {}
max_download = {}

previous_time = 0

for commit in repo.iter_commits(paths=file_path, reverse=True):
	cnt += 1
	file_content = commit.tree[file_path].data_stream.read().decode('utf-8')

	#print('Time: ' + str(commit.committed_datetime))

	version_data = json.loads(file_content)

	if int(commit.committed_datetime.timestamp()) == 1675602142:
		continue

	data.append({
		#'time': int(commit.committed_datetime.timestamp()),
		'delta_time': int(commit.committed_datetime.timestamp()) - previous_time,
		'download': {}
	})
	previous_time = int(commit.committed_datetime.timestamp())

	for plugin in version_data:
		data[-1]['download'][plugin['name']] = int(plugin['count'])
		if plugin['name'] not in slugs:
			slugs.append(plugin['name'])
		last_download[plugin['name']] = int(plugin['count'])
		max_download[plugin['name']] = max(max_download.get(plugin['name'], 0), int(plugin['count']))
	
	# if (cnt == 1): print(data)

#print(cnt)

slugs.sort(key=lambda slug: last_download[slug], reverse=True)
slugs = [slug for slug in slugs if max_download[slug] >= 20]
slugs = [slug for slug in slugs if last_download[slug] >= 20]
#print(slugs)


output = []

for slug in slugs:
	node = {
		'name': slug,
		'type': 'line',
		'smooth': True,
      	'symbol': 'none',
		'data': []
	}
	previous_download = 0
	for version in data:
		if slug in version['download']:
			#node['data'].append([version['time'], version['download'][slug]])
			node['data'].append([version['delta_time'], version['download'][slug] - previous_download])
			previous_download = version['download'][slug]
		else:
			#node['data'].append([version['time'], ''])
			node['data'].append([version['delta_time'], ''])
			previous_download = 0
	
	output.append(node)


with open('./chart/data.js', 'w') as f:
	outJson = json.dumps(output, separators=(',', ':'))
	outJson = outJson.replace('],[', '~');
	outJson = outJson.replace(',""~', '$');
	f.write('var data = `' + outJson + '`;')
