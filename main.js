const rootEndpoint = '/repos/nss-maps/nss-maps.github.io';

export async function start(Octokit) {
  const octikit = new Octokit();
  const repoData = await octikit.request(rootEndpoint);
  const contentData = await octikit.request(repoData.data.contents_url, {
    path: 'maps'
  });
  console.log(contentData);
}