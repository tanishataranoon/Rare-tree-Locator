document.addEventListener("DOMContentLoaded", () => {
  let loadBtn = document.querySelector(".load-more a");

  loadBtn?.addEventListener("click", function(e){
      e.preventDefault();
      fetch(this.href)
      .then(res => res.text())
      .then(data => {
          let parser = new DOMParser();
          let htmlDoc = parser.parseFromString(data, "text/html");
          let newPosts = htmlDoc.querySelector(".grid").innerHTML;
          document.querySelector(".grid").innerHTML += newPosts;

          let newLoad = htmlDoc.querySelector(".load-more a");
          if (newLoad) {
              this.href = newLoad.href;
          } else {
              this.remove();
          }
      });
  });
});
