!(function () {
  'use strict'

  class Person {
    constructor(options){
      this.name = options.name
      this.code = options.code
      this.award_type = options.type
      this.url = options.url
      this.isRun = false
    }
  }
  class Winner {
    constructor(){

    }
  }
  class AwardType {
    constructor(options){
      this.type = options.type||''
      this.total = options.total
      this.singleNum = options.singleNum
      this.takeNum = 0
    }
  }

  class Turntable {
    constructor(){
      this.container = $('#galleryWrap')
      this.persons = []
      this.init()
    }

    init = () => {
      let self = this;
    }

    updatePersons = (persons) => {
      this.persons = persons
      this.renderDom()
    }

    renderDom = () => {
      let fragment = document.createDocumentFragment()
      this.persons.forEach(p=>{
        var oA = document.createElement('a')
        oA.herf = 'javascript:;'
        oA.setAttribute('data-url',p.url)
        oA.setAttribute('data-type',p.isRun?'1':'0')
        oA.style.backgroundImage = `url('${p.url}')`
        var oLi = document.createElement('li')
        oLi.appendChild(oA)
        fragment.appendChild(oLi)
      })
    }

    run = ()=>{

    }

    stop = ()=>{

    }

    isFinished = () => {
      return this.persons.some(p=>!p.isRun)
    }
  }

  class Lottery {
    constructor(){
      this.persons = []
      this.winners = []
      this.awardMap = {}
      this.init()
    }
    init = () => {
      this.preLoadData(()=>{
        this.renderButtonList()
        this.attachEvent()
      })
    }
    attachEvent = () => {
      let self = this
      $('#cirle-btn').click(function(){

      })
      
      
      $('#active').click(function(){

      })

    }
    preLoadData = (callback) => {
      let self = this
      let url = './data.json'

      let request = new XMLHttpRequest()
      request.open('get', url)
      request.send(null)
      request.onload = function () {
        if (request.status == 200) {

          let data = JSON.parse(request.responseText)

          data.lottery_type_order.split(',').forEach(type =>{
            self.awardMap[type] = new AwardType({

            })
          })
        
          let list = Object.values(data.persons)
          let promiseAll = []
          list.forEach((item,index)=>{
            let promise = new Promise((resolve, reject)=>{
              let img = new Image()
              img.onload = function () {
                resolve(img)
              }
              img.error = function () {
                console.error(item)
                reject('图片加载失败')
              }
              img.src = item.url.replace(/^\//, '')
            })
            promiseAll.push(promise)

            let person = new Person({
              name:item.c_name || item.e_name,
              e_name:item.e_name,
              code:index,
              type:item.join_type,
              url:item.url
            })
            self.persons.push(person)


          })
          Promise.all(promiseAll).then(()=>{
            console.log('加载图片完成')
          },(err)=>{
            console.log('加载图片出错')
          })
        
        }
        callback();
      }
    }

  }

  new Lottery()

})()