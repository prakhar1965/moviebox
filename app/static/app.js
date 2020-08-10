Vue.component('star-rating', VueStarRating.default)
       var vm = new Vue({
         delimiters: ["[[","]]"],
         el: '#app',
         data() {
           return {
           prefix: "",
           url : "/api/get-movies/",
           results: null,
           ratings: {},
           re_movies: null
         }
         },
         methods: {
           getResults: function () {
             axios.get(this.url+this.prefix)
             .then(response => {
              this.results = response.data
            })
           },
          addrating: function (rating,item) {
             this.prefix = ""
             item['rating'] = rating
             item_id = item['index']
             Vue.set(this.ratings,item_id,item)
             this.recommendations()
          },
          removemovie: function (item) {
             this.prefix = ""
             item_id = item['index']
             Vue.delete(this.ratings,item_id)            
             this.recommendations()
          },
          recommendations: function(){
            this.re_movies = null
            axios.post('/api/get-recommendation', {
            watched_movies: this.ratings
          })
            .then(response => {
            
            this.re_movies = response.data
          })
            .catch(function(e) {
              console.log("Error:",e)
            });
          }
         },
         // declare Vue watchers
        watch: {
         // watch for change in the query string and recall the search method
         prefix: function() {
          if(this.prefix.length === 0){
          this.results = null
        }
          else{
          this.getResults();
        }
      }
      }
      });