const rootEndpoint = '/repos/nss-maps/nss-maps.github.io';

export async function start(Octokit) {
  const octikit = new Octokit();
  const repoResponse = await octikit.request(rootEndpoint);
  const fetchContent = contentFetcher(octikit, repoResponse.data.contents_url);

  const mapCollectionContent = await fetchContent('maps');
  renderMapCollections(await toMapCollections(mapCollectionContent, fetchContent));
}

function contentFetcher(octikit, contentUrl) {
  return (path) => octikit.request(contentUrl, { path });
}

async function toMapCollections(mapCollectionContent, fetchContent) {
  const collectionPromises = mapCollectionContent.data
    .filter(d => d.type === 'dir')
    .map(async d => {
      const mapContent = await fetchContent(d.path);
      return {
        name: d.name,
        path: d.path,
        maps: toMapCollection(mapContent)
      }
    });

  return await Promise.all(collectionPromises);
}

function toMapCollection(mapContent) {
  return mapContent.data.map(m => ({ name: m.name, path: m.path }));
}

function renderMapCollections(collections) {
  const el = document.getElementById('map-collections');
  el.innerHTML = mapCollectionsHtml(collections);
}

function mapCollectionsHtml(collections) {
  return (
    `<article class="map-collection"> 
      ${collections
      .map(col =>
        `<header class="map-collection__header">
              ${col.name}
            </header>
            ${mapCollectionHtml(col)}
            `)
      .join('')}
     </article>`
  );
}


function mapCollectionHtml(collection) {
  return (
    collection.maps
      .map(m => `
        <section class="map">
          <a href="${m.path}" target="_new">${m.name}</a>
        </section>`)
      .join('')
  );
}