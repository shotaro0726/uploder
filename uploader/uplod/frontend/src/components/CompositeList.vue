<template>
    <section id="composites">
       <div v-if="current.parent" class="parent composite-wrapper" :key="current.parent.pk">
            <p class="composite" @click="moveBefore">{{ current.parent.name }}</p>
        </div>
        <div v-else-if="current.pk" class="parent composite-wrapper" :key="-1">
            <p class="composite" @click="moveTop">home</p>
        </div>

        <div v-if="current.pk" class="current composite-wrapper" :key="current.pk">
            <p class="composite">{{ current.name }}</p>
        </div>
        <div v-else class="current composite-wrapper" :key="-1">
            <p class="composite">home</p>
        </div>

        <div class="child composite-wrapper" v-for="composite of current.composite_set" :key="composite.pk">
            <p class="composite" @click="move(composite)">{{ composite.name }}</p>
        </div>
    </section>
</template>

<script>
    export default {
        name: 'composite-list',
        props: {
            path:{type: String},
        },
        data() {
            return {
                current: {},
            }
        },
        created() {
           if(this.path) {
               this.getCompositeListFromPath(this.path)
           } else {
               this.getCompositeListTop()
           }
        },
        method: {
            getCompositeListTop() {
                this.$http(this.$endpoint)
                .then(response => {
                    return response.json()
                })
                .then(data => {
                    this.current = {
                        composite_set: data
                    }
                })
            },
            getCompositeListFromPk(pk) {
                this.$http(this.$endpoint + pk + '/')
                .then(reponse => {
                    return response.json()
                })
                .then(data => {
                    this.current = data
                }) 
            },
            getNextPath(composite) {
                let basePath = this.$route.path
                if(!basePath.endsWith('/')) {
                    basePath = basePath + '/'
                }
                let nextPath = basePath + composite.name
                if(composite.is_dir) {
                    nextPath = nextPath + '/'
                }
                return nextPath
            },
            getBeforePath() {
                const paths = []
                for (const path of this.$route.path.split('/')){
                    if(path) {
                        paths.push(path)
                    }
                }
                paths.pop()
                return '/' + paths.join('/') + '/'
            },
            getCompositeListFromPath(path) {
                this.$http(this.$endpoint + 'get_composite_from_path/' + path)
                .then(response => {
                    return response.json()
                })
                .then(data => {
                    this.current = data
                })
            },
            move(composite) {
                const nextPath = this.getNextPath(composite)
                if (!composite.is_dir) {
                    window.open(`http://127.0.0.1:8000/uplod${nextPath}`,'_blank')
                }else{
                    this.$router.push(nextPath)
                    this.getCompositeListFromPk(composite.pk)
                }
            },
            moveTop(){
                this.getCompositeListTop()
            },
            moveBefore() {
                const beforePath = this.getBeforePath()
                this.$router.push(beforePath)
                this.getCompositeListFromPk(this.current.parent.pk)
            },
        },
    }
</script>

<style scoped>
  .composite-wrapper {
      margin-bottom: 50px;
  }
  .current {
      background-color: #ffff;
      padding: 6px;
  }

  @media (min-width: 1024px) {
      #composites {
          padding-top: 120px;
      }
      .current > composite {
          margin-left: 50px;
      }
      .cjild {
          margin-left: 100px;
      }
  }
</style>