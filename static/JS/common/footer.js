function navigate(page) {
  switch(page) {
    case 'home':
      window.location.href = 'index.html';
      break;
    case 'trees':
      window.location.href = 'trees.html';
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
