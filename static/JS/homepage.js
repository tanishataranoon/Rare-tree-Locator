const featuredTrees = [
  {
    id: 1,
    name: "Ancient Forest Giant",
    image: "https://images.unsplash.com/photo-1566524802776-d5b8997f7c68?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
    category: "Endangered"
  },
  {
    id: 2,
    name: "Majestic Oak",
    image: "https://images.unsplash.com/photo-1653322462059-605b749a16e1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
    category: "Native"
  },
  {
    id: 3,
    name: "Cherry Blossom Beauty",
    image: "https://images.unsplash.com/photo-1526344966-89049886b28d?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
    category: "Flowering"
  },
  {
    id: 4,
    name: "Towering Redwood",
    image: "https://images.unsplash.com/photo-1562633243-28d2b1556b13?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080",
    category: "Native"
  }
];

// Render tree cards
const treeContainer = document.getElementById('featured-trees');

featuredTrees.forEach(tree => {
  const card = document.createElement('div');
  card.classList.add('tree-card');
  card.onclick = () => navigate('trees');
  card.innerHTML = `
    <img src="${tree.image}" alt="${tree.name}">
    <div class="tree-info">
      <div class="tree-name">${tree.name}</div>
      <div class="tree-category">${tree.category}</div>
    </div>
  `;
  treeContainer.appendChild(card);
});

// Navigation function
function navigate(page) {
  switch(page) {
    case 'home':
      window.location.href = 'index.html';
      break;
    case 'trees':
      window.location.href = 'trees.html';
      break;
    case 'profile':
      window.location.href = 'profile.html';
      break;
    case 'blog':
      window.location.href = 'blog.html';
      break;
    case 'signup':
      window.location.href = 'signup.html';
      break;
    default:
      console.log('Page not found:', page);
  }
}
