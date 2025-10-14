document.addEventListener('DOMContentLoaded', () => {
  const nav = document.getElementById('category-nav');
  const content = document.getElementById('content');
  const searchInput = document.getElementById('search');
  const searchResults = document.getElementById('search-results');

  let categoryMap = null;
  const navStack = [];

  const basePath = window.location.origin + window.location.pathname.replace(/\/[^\/]*$/, '/');

  Promise.all([
    fetch(basePath + 'data/category_map.json').then(res => res.json()),
    fetch(basePath + 'data/index.json').then(res => res.json())
  ]).then(([map, recipes]) => {
    categoryMap = map;
    renderCategories(categoryMap);
    setupSearch(recipes);
  });

  function createBackButton() {
    const backBtn = document.createElement('button');
    backBtn.textContent = '← Tilbage';
    backBtn.className = 'back-button';
    backBtn.addEventListener('click', () => {
      const previous = navStack.pop();
      if (!previous || previous.view === 'home') {
        resetToHome();
      } else if (previous.view === 'category' && previous.category) {
        loadCategory(previous.category);
      } else if (previous.view === 'search' && previous.searchQuery) {
        restoreSearch(previous.searchQuery);
      }
    });
    return backBtn;
  }

  function resetToHome() {
    content.innerHTML = '';
    searchResults.innerHTML = '';
    searchInput.value = '';
    nav.innerHTML = '';
    renderCategories(categoryMap);
  }

  function renderCategories(map) {
    nav.innerHTML = '';
    nav.classList.add('category-list');

    Object.entries(map).forEach(([folderName, displayName]) => {
      const pane = document.createElement('div');
      pane.className = 'category-pane';
      pane.textContent = displayName;

      pane.addEventListener('click', () => {
        navStack.push({ view: 'home' });
        loadCategory(displayName);
      });

      nav.appendChild(pane);
    });
  }

  function loadCategory(displayName) {
    fetch(basePath + 'data/index.json')
      .then(res => res.json())
      .then(recipes => {
        const filtered = recipes.filter(r => r.category === displayName);

        content.innerHTML = '';
        nav.innerHTML = '';
        searchResults.innerHTML = '';
        searchInput.value = '';

        const header = document.createElement('div');
        header.className = 'category-header';

        const title = document.createElement('h2');
        title.textContent = displayName;

        const back = document.createElement('a');
        back.className = 'back-link';
        back.textContent = '← Tilbage';
        back.href = '#';
        back.addEventListener('click', e => {
          e.preventDefault();
          resetToHome();
        });

        header.appendChild(title);
        header.appendChild(back);
        content.appendChild(header);

        const list = document.createElement('ul');
        list.className = 'recipe-list';

        filtered.forEach(recipe => {
          const item = document.createElement('li');
          item.textContent = recipe.title;
          item.addEventListener('click', () => {
            navStack.push({ view: 'category', category: displayName });
            loadRecipe(recipe.path);
          });
          list.appendChild(item);
        });

        content.appendChild(list);
      });
  }

  function loadRecipe(path) {
    fetch(basePath + path)
      .then(res => res.text())
      .then(md => {
        const stripped = md.replace(/^# .*\n/, '');
        content.innerHTML = '';

        const backBtn = createBackButton();
        const recipeWrapper = document.createElement('div');
        recipeWrapper.className = 'recipe-content';
        recipeWrapper.innerHTML = marked.parse(stripped);

        content.appendChild(backBtn);
        content.appendChild(recipeWrapper);
      });
  }

  function setupSearch(recipes) {
    searchInput.addEventListener('input', () => {
      const query = searchInput.value.trim().toLowerCase();
      searchResults.innerHTML = '';
      content.innerHTML = '';
      nav.innerHTML = '';

      if (query.length === 0) return;

      navStack.push({ view: 'home' });

      const header = document.createElement('div');
      header.className = 'search-header';

      const title = document.createElement('h2');
      title.textContent = `Søgeresultater for: "${query}"`;

      const back = document.createElement('a');
      back.className = 'back-link';
      back.textContent = '← Tilbage';
      back.href = '#';
      back.addEventListener('click', e => {
        e.preventDefault();
        resetToHome();
      });

      header.appendChild(title);
      header.appendChild(back);
      content.appendChild(header);

      const matches = recipes.filter(recipe =>
        recipe.tags && recipe.tags.some(tag => tag.includes(query))
      );

      matches.forEach(recipe => {
        const item = document.createElement('li');
        item.textContent = recipe.title;
        item.addEventListener('click', () => {
          searchResults.innerHTML = '';
          navStack.push({ view: 'search', searchQuery: query });
          loadRecipe(recipe.path);
        });
        searchResults.appendChild(item);
      });
    });
  }

  function restoreSearch(query) {
    searchInput.value = query;
    content.innerHTML = '';
    nav.innerHTML = '';
    searchResults.innerHTML = '';

    const header = document.createElement('div');
    header.className = 'search-header';

    const title = document.createElement('h2');
    title.textContent = `Søgeresultater for: "${query}"`;

    const back = document.createElement('a');
    back.className = 'back-link';
    back.textContent = '← Tilbage';
    back.href = '#';
    back.addEventListener('click', e => {
      e.preventDefault();
      resetToHome();
    });

    header.appendChild(title);
    header.appendChild(back);
    content.appendChild(header);

    fetch(basePath + 'data/index.json')
      .then(res => res.json())
      .then(recipes => {
        const matches = recipes.filter(recipe =>
          recipe.tags && recipe.tags.some(tag => tag.includes(query))
        );

        matches.forEach(recipe => {
          const item = document.createElement('li');
          item.textContent = recipe.title;
          item.addEventListener('click', () => {
            searchResults.innerHTML = '';
            navStack.push({ view: 'search', searchQuery: query });
            loadRecipe(recipe.path);
          });
          searchResults.appendChild(item);
        });
      });
  }
});
