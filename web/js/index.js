!(function () {
  'use strict'
  const startText = '立即抽奖', // 开始按钮文案
        stopText = '暂停' // 停止按钮文案

  var AwardEnum;

  (function (AwardEnum) {
    AwardEnum[AwardEnum["s1"] = 'f1'] = "s1";
    AwardEnum[AwardEnum['s2'] = 'f2'] = "s2";
    AwardEnum[AwardEnum["0"] = 's'] = "0";
    AwardEnum[AwardEnum["1"] = '1'] = "1";
    AwardEnum[AwardEnum["2"] = '2'] = "2";
    AwardEnum[AwardEnum["3"] = '3'] = "3";
    AwardEnum[AwardEnum["4"] = '4'] = "4";
    AwardEnum[AwardEnum["5"] = '5'] = "5";
  })(AwardEnum || (AwardEnum = {}));

  function Enum() {
  }

  // 除chrome外，其他支持需要在服务器上运行才支持
  if (!window.localStorage) {
    alert('不支持localstorage，抽奖无法启动！')
  }
  // 处理 localstorage 中奖数据
  let local_handle = {
    local_item: 'lottery_datas',
    get(key) {
      let val = window.localStorage.getItem(key)
      if (val) {
        return JSON.parse(val)
      }
      return ''
    },
    set(key, val) {
      window.localStorage.setItem(key, JSON.stringify(val))
    },
    delete(datas, name) {
      let res = []
      datas.forEach((val, index) => {
        if (name != val.nameen) {
          res.push(val)
        }
      })
      let new_datas = JSON.stringify(res)
      this.set(this.local_item, new_datas)
      return res
    },
    clear() {
      window.localStorage.clear()
    }
  }

  // 音乐数据
  let music_config = {
    music: document.getElementById('music'),
    music_bool: false,
    init() {
      if (this.music_bool) {
        this.play()
      } else {
        this.music.pause()
      }
    },
    play() {
      this.music.play()
      $('#musicButton').addClass('open-button')
      this.music_bool = true
    },
    pause() {
      this.music.pause()
      $('#musicButton').removeClass('open-button')
      this.music_bool = false
    }
  }
  music_config.init()

  class Base {
    /**
     * 判断类型
     * @param obj
     * @returns {string|boolean}
     */
    typeof = obj => {
      try {
        let type = Object.prototype.toString.call(obj)
        if (type === '[object Array]') {
          return 'Array'
        } else if (type === '[object Object]') {
          return 'Object'
        } else if (type === '[object Number]') {
          return 'Number'
        } else if (type === '[object String]') {
          return 'String'
        } else if (type === '[object Boolean]') {
          return 'Boolean'
        } else if (type === '[object Function]') {
          return 'Function'
        }
      } catch (e) {
        console.error(e)
      }
      return false
    }

    /**
     * 产生一个随机数
     * @param number
     * @returns {number}
     * Math.ceil(Math.random()*10);     // 获取从 1 到 10 的随机整数，取 0 的概率极小。
     * Math.round(Math.random());       // 可均衡获取 0 到 1 的随机整数。
     * Math.floor(Math.random()*10);    // 可均衡获取 0 到 9 的随机整数。
     * Math.round(Math.random()*10);    // 基本均衡获取 0 到 10 的随机整数，其中获取最小值 0 和最大值 10 的几率少一半。
     */
    random = number => {
      try {
        if (this.typeof(number) === 'Number') {
          return Math.floor(Math.random() * number)
        }
      } catch (e) {
        console.error(e)
      }
      return 0
    }

    /**
     * 随机获取 n 位数
     * @param arr
     * @param count
     * @returns {T[]}
     */
    getRandomArrayElements = (arr, count) => {
      let shuffled = arr.slice(0),
        i = arr.length,
        min = i - count,
        temp, index
      while (i-- > min) {
        index = Math.floor((i + 1) * Math.random())
        temp = shuffled[index]
        shuffled[index] = shuffled[i]
        shuffled[i] = temp
      }
      return shuffled.slice(min)
    }
  }

  class Winner {
    constructor(type, person) {
      this.type = type
      this.person = person
    }
  }

  class AwardType {
    constructor(options) {
      this.type = options.type || '';   //抽奖类型 一等奖二等奖等等
      this.total = options.total || 1;  //总数
      this.single_num = options.single_num || 1;  //每次抽几个人
      this.take_num = options.take_num || 0;  //  已经抽了多少个人
      this.personInfos = [];  // 本类型总共的抽奖人员
      this.winners = [];  // 获奖者
      // this.isRun = false; // 是否已经抽过
    }
    isFinished = () => {
      if (this.personInfos.some(item => !item.isRun)) {
        return false
      }
      return true
    }
    clearInfo = () => {
      this.take_num = 0;
      this.winners = [];
    }
    setWinners = (winners) => {
      if (winners.length < 1) {
        return
      }
      this.take_num += winners.length;
      this.winners = this.winners.concat(winners);
      this.personInfos = this.personInfos.filter((info) => {
        return this.winners.indexOf(info) < 0;
      })
    }
    addPerson = (person) => {
      this.personInfos.push(person);
    }
  }

  class Lottery extends Base {
    constructor(props) {
      super(props)
      this.state = {
        typeMap: {},
        typeArr: [],
        winners: [],
        award: null, // 当前奖项·· 1 一等奖，2二等奖， 3三等奖 4 优二 5 优一
        award_num: 0, // 奖项数量
        persons: [],
        file_list: [], // 图片数据
        file_total: 0, // 图片总数
        awardFileMap: {
          award4: [],
          award5: []
        },
        awardMan: null,
        photo_row: 4, // 行数
        photo_col: 10, // 列数
        photo_num: 0, // 显示总数
        photos: [] // 显示的图片
      }

      // [图片总数] 必须大于 [显示总数]
      this.state.photo_num = this.state.photo_row * this.state.photo_col

      // 奖项对应抽奖数量
      /**
       三等奖。38个三次出 13 13 12

       二等奖：16个，两次出，8、8出

       一等奖：三个，分三次出，一次出一个

       特等奖，一个，一次出
       */
      // this.winnerNumber = [[1], [1, 1, 1], [8, 8], [13, 13, 12],[1],[1]]
    }
    /**
      * 设置 state
      * @param obj
      */
    setState = (obj, callback) => {
      if (this.typeof(obj) === 'Object') {
        this.state = Object.assign(this.state, obj)
        callback && this.typeof(callback) === 'Function' && callback()
      }
    }

    /**
     * 获取图片数据
     * @param callback
     */
    fetchPhotoList = (callback) => {
      const { photo_num } = this.state
      const self = this
      let url = 'http://localhost:8888/'
      let request = new XMLHttpRequest()
      request.open('get', url)
      request.send(null)
      request.onload = function () {
        if (request.status == 200) {
          let data = JSON.parse(request.responseText)
          console.log(data)
          let typeMap = {}
          let types = data.lottery_type_order.split(',')
          types.forEach((type) => {
            type = type.toLocaleLowerCase();
            typeMap[type] = new AwardType({
              type,
              total: +data[`prize${type}_total_num`] || 1,//prize1_total_num
              single_num: +data[`prize${type}_take_count`] || 1,
            })
            if (type == 's1' || type == 's2') {
              typeMap[type].total = data[`special_prize${type[1]}_person`].split(",").length
            }
          })
          console.log(typeMap)
          let persons = Object.values(data.persons)
          self.photoPreload(persons)
          persons.forEach((p, index) => {
            p.code = index
            p.isRun = false
            let type = p.join_type.toLocaleLowerCase()
            if (type == 's1' || type == 's2') {
              typeMap[type].addPerson(p)
            }
          });
          self.setState({
            typeMap,
            persons
          })
        }
        callback && self.typeof(callback) === 'Function' && callback()
      }
    }

    /**
      * 图片预加载
      * @param fileList
      */
    photoPreload = (fileList, callback) => {
      let self = this
      let promiseAll = fileList.map(item => {
        return new Promise((resolve, reject) => {
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
      })

      // 图片 预加载
      Promise.all(promiseAll).then(() => {
        callback && self.typeof(callback) === 'Function' && callback()
        console.log('图片加载完毕')
      }, (err) => {
        console.log(err)
      })
    }

    /**
     * 更新图片数据
     * @param award
     * @param winners
     */
    updatePhotoList = (award, winners) => {
      if (award == 's1' || award == 's2') {
        return
      }
      if (award !== null && winners && winners.length) {
        const { photo_num, file_list } = this.state
        // 用过滤的方式得到新图片数据
        let fileList = file_list.filter((item, index) => !winners.includes(index))
        let file_total = fileList.length - 1
        // 更新state
        this.setState({
          file_list: fileList,
          file_total,
          photo_num: file_total < photo_num ? file_total : photo_num // 控制显示图片最大数量
        })
      }
    }

    addWinners = (ws) => {
      let { winners } = this.state
      winners = winners.concat(ws)
      this.setState({
        winners
      })
    }

    /**
     * 保存中奖者信息
     * @param award
     * @param winners
     */
    saveWinnerInfo = (award, winners) => {
      console.log("winners", winners)
      this.addWinners(winners)
      if (award !== null && winners && winners.length) {
        // 获取本地中奖信息
        let winnerName = `award_${award}`
        let winnerInfo = local_handle.get(winnerName) || []
        // 把中奖者信息保存在本地
        local_handle.set(winnerName, winnerInfo.concat(winners))
        var list_names = winners.map(function (item) {
          return item.e_name
        })
        var param = {}
        param['win_type'] = winnerName.split("_")[1]
        param['lucky_dogs'] = list_names

        $.ajax({
          method: 'post',
          url: 'http://localhost:8888/lucky_dog',
          data: JSON.stringify(param),
          success: function (res) {
            if (res.code == '0000') {
            } else {
              alert(res.desc)
            }
          },
          error: function (res) {
              alert('请求失败')
          }
        })
      }
    }

    getValidFileList = (award) => {
      let { persons, typeMap, winners } = this.state
      award = '' + award
      return persons.filter(person => {
        if (winners.some(w => w.code === person.code)) {
          return false
        }
        if (award === 's1' || award === 's2') {
          return person.join_type.toLocaleLowerCase() === award
        }
        if (award === '1') {
          return person.join_type.toLocaleLowerCase() !== 's1'
        }
        if (award === '2') {
          return person.join_type.toLocaleLowerCase() !== 's2'
        }
        return true;
      })

    }
    /**
     * 获取随机图片(下标)
     * @returns {Array}
     */
    getRandomPhoto = () => {
      try {
        const { file_total, photos } = this.state
        let index = this.random(file_total)

        if (photos.includes(index)) { // 包含控制
          return this.getRandomPhoto() // 重新获取
        } else {
          return index
        }
      } catch (e) {
        console.error(e)
        return 0
      }
    }

    /**
     * 获取显示图片数据(下标)
     * @returns {Array}
     */
    getPhotoData = () => {
      const { photo_num } = this.state

      try {
        let list = []
        for (let i = 1; i <= photo_num; i++) {
          list.push(this.getRandomPhoto())
          this.setState({
            photos: list
          })
        }
      } catch (e) {
        console.error(e)
      }
    }

    /**
     * 获取显示图片
     * @param index
     * @returns {void | string | never|string}
     */
    getPhoto = (index) => {
      const { file_list } = this.state
      if (file_list.length == 1) {
        index = 0
      }
      try {
        if (index !== undefined) {
          let photoInfo = file_list[index]
          let photo = photoInfo.url.replace(/^\//, '')
          return photo
        }
      } catch (e) {
        console.error(e)
      }
      return ''
    }

    renderButton = () => {
      let { typeMap } = this.state
      let wrap = document.createDocumentFragment();
      for (let type in typeMap) {
        // <div class="cirle-btn award" id="award-2" data-award="2">二</div>
        let oDiv = document.createElement('div')
        oDiv.className = 'cirle-btn award'
        oDiv.id = `award-${type}`
        oDiv.setAttribute('data-award', type)
        oDiv.innerText = AwardEnum[type]
        console.log(oDiv)
        wrap.appendChild(oDiv)
      }
      console.log(wrap)
      $('.custom-draw')[0].appendChild(wrap)
    }

    /**
     * 渲染
     */
    render = () => {
      const { award, photo_num, file_total, typeMap, file_list } = this.state
      const { personInfos } = typeMap[award]
      let loadedIndex = 1
      // 图片渲染
      let fragmentEle = document.createDocumentFragment()
      // 优一优二， 显示的图片下标是固定的，不是随机的
      if (award == 's1' || award == 's2') {
        this.setState({ photos: file_list.map(function (n, index) { return index }) })
      }
      const { photos } = this.state
      // console.log('初始化图片', personInfos,photos,file_list)

      $('#gallery')[0].innerHTML = ''
      $.each(photos, (index, photo) => {
        /* 此方式会将图片一并输出*/
        let link = document.createElement('a'),
          li = document.createElement('li')

        link.href = 'javascript:;'
        link.classList.add('person_image')
        link.setAttribute('data-index', photo)
        link.style.backgroundImage = `url('${this.getPhoto(photo)}')`
        li.appendChild(link)
        if (award !== 's1' && award !== 's2') {
          $('#gallery')[0].appendChild(li)
        } else {
          fragmentEle.appendChild(li);
        }
        setTimeout(() => {
          $(li).addClass('loaded')
        }, 10 * loadedIndex++)

      })
      $('.galleryWrap')[0].innerHTML = ''
      if (award !== 's1' && award !== 's2') {
      } else {
        $('.galleryWrap')[0].appendChild(fragmentEle);
      }
      if (photo_num < file_total) { // 执行动画条件
        this.animatedBounce()
      } else {
        //alert('[图片总数] 必须大于 [显示总数]')
      }
    }

    /**
     * 重新渲染
     */
    reRender = () => {
      if (this.timer_small_slow) { // 停止切换图片
        clearInterval(this.timer_small_slow)
      }
      if (this.timer_fast) { // 停止快速切换图片
        clearInterval(this.timer_fast)
      }
      $('#action').data('action', 'start').html(startText)

      this.clearStyle()

      if (!this.state.photos.length) {
        return false
      }

      // 图片重新渲染,优一优二不重置
      // this.setState({photos:file_list.map(function(n,index){return index})})
      this.setState({
        photos: []
      })
      this.getPhotoData()
      const { photos, photo_num, file_total } = this.state
      let loadedIndex = 1

      // 图片渲染
      console.log('重新渲染图片', photos, photo_num, file_total)

      $('#gallery li').each((index, item) => {
        $(item).removeClass('loaded')
        let photo = photos[index]
        if (photo === undefined) {
          $(item).remove() // 缺少图片删除
        } else {
          $(item)
            .removeClass('animated bounce')
            .find('a')
            .attr('style', `background-image: url('${this.getPhoto(photo)}')`)
        }

        setTimeout(() => {
          $(item).addClass('loaded')
        }, 25 * loadedIndex++)
      })

      if (photo_num < file_total) { // 执行动画条件
        this.animatedBounce()
      } else {
        // alert('[图片总数] 必须大于 [显示总数]')
      }
    }

    /**
     * 开启切换图片
     */
    animatedBounce = () => {
      const {
        photo_num,
        photos
      } = this.state

      let self = this
      self.timer_small_slow = setInterval(() => {
        try {
          let rendomLi = self.random(photo_num)
          $(`#gallery li:eq(${rendomLi})`)
            .addClass('animated bounce')
            .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function () {
              let photo = self.getRandomPhoto() // 随机图片下标
              photos[rendomLi] = photo // 替换图片下标
              self.setState({
                photos
              })
              $(this)
                .removeClass('animated bounce')
                .find('a')
                .attr('style', `background-image: url('${self.getPhoto(photo)}')`)
            })
        } catch (e) {
          console.error(e)
        }
      }, 50)
    }

    /**
     * 添加操作事件
     */
    event = () => {
      let self = this

      // 按钮控制器
      $(document).keypress((event) => {
        if (event.target.id !== 'wardNumber') {
          console.error(event.which)
          switch (event.which) {
            case 13: // [enter | 回车键]
            case 32: // [spacing | 空格键]
              // 控制开始和停止
              $('#action').click()
              break
            case 48: // [0键] - 重新渲染
              console.error('0键')
              self.reRender()
              break
            case 49: // [1键] - 一等奖
              console.error('1键')
              self.setWinner('1')
              break
            case 50: // [2键] - 二等奖
              console.error('2键')
              self.setWinner('2')
              break
            case 51: // [3键] - 三等奖
              console.error('3键')
              self.setWinner('3')
              break
            case 52: // [4键] - 特等奖
              console.error('4键')
              self.setWinner('0')
              break
            case 53: // [5键]
              console.error('5键')
              break
            case 54: // [6键]
              console.error('6键')
              break
            case 55: // [7键]
              console.error('7键')
              break
            case 56: // [8键] - 音乐开关
              console.error('8键')
              if (music_config.music_bool) {
                music_config.pause()
              } else {
                music_config.play()
              }
              break
            case 57: // [9键]
              console.error('9键')
              self.setState({ award: null })
              break
            default:
              return false
          }
        }
      })

      $('#action').click(function () {
        if (self.timer_small_slow) { // 停止切换图片
          clearInterval(self.timer_small_slow)
        }
        $(`#gallery li:eq(0) a`).attr('style', `background-image: url('')`)

        if ($(this).data('action') == 'start') { // 开始

          let { award, awardMan, photos, photo_num, file_total, file_list, typeMap } = self.state
          // console.log($(this).data('action'),self.state.typeMap,self.state.typeMap[award],self.state.awardMan,self.state.file_list)
          self.clearWinner()
          if (award == 's1' || award == 's2') {

            if (awardMan == null) {
              alert('请先选择抽奖人')
              return
            }
            if (self.state.typeMap[award].personInfos[awardMan].isRun) {
              alert('当前选择人已经抽过奖，不能重复抽奖')
              return
            }
            self.state.typeMap[award].personInfos[awardMan].isRun = true
            $(this).data('action', 'stop').html(stopText)
            self.startRun()
            return;
          }
          console.log(typeMap)
          if (typeMap[award].take_num >= typeMap[award].total) {
            alert('人数抽够了！')
            return false
          }
          if (!photos.length) {
            alert('没有抽奖候选人')
            return false
          }
          $(this).data('action', 'stop').html(stopText)
          if (photo_num < file_total) { // 执行动画条件
            if (self.timer_fast) { // 停止快速切换图片
              clearInterval(self.timer_fast)
            }
            // 快速切换图片
            self.timer_fast = setInterval(() => {
              let rendomLi = self.random(photo_num)
              let photo = self.getRandomPhoto() // 随机图片下标
              photos[rendomLi] = photo // 替换图片下标
              self.setState({
                photos
              })
              $(`#gallery li:eq(${rendomLi}) a`).attr('style', `background-image: url('${self.getPhoto(photo)}')`)
            }, 5)
          }
        } else { // 停止
          self.stopRun()
          clearInterval(self.timer_fast)
          $(this).data('action', 'start').html(startText)
          // console.log(award, winners)
          self.getWinner()
        }
      })

      // 音乐开关
      $('#musicButton').click(() => {
        if (music_config.music_bool) {
          music_config.pause()
        } else {
          music_config.play()
        }
      })

      // 清除数据开关
      $('#clearButton').click(() => {
        let sure = confirm('警告：确定清除所有数据？！')
        if (sure) {
          local_handle.clear()
          window.location.reload()
          $.ajax({
            method: 'get',
            url: 'http://localhost:8888/reset',
            success: function (res) {
              if (res.code == '0000') {
                alert("重置成功")
              } else {
                alert(res.desc)
              }
            },
            error: function (res) {
              alert('请求失败')
            }
          })
        }
      })
      // 自定义奖品选择
      $('.cirle-btn').click(function () {
        let { typeMap, award } = self.state
        if (award == 's1' || award == 's2') {
          if (!typeMap[award].isFinished()) {
            alert('当前奖项的参与人数还有没参与抽奖的!')
            return;
          }
        }
        award = $(this).data('award')
        if (award != 's1' && award != 's2') {
          if ((typeMap['s1'] && !typeMap['s1'].isFinished()) || (typeMap['s2'] && !typeMap['s2'].isFinished())) {
            alert('请先进行优等抽奖!')
            return
          }
          $('#gallery').show();
          $('#gallery-one').hide();
        } else {
          $("#gallery-one .item").removeClass('active')
          $('#gallery').hide();
          $('#gallery-one').show();
        }
        $('.cirle-btn').removeClass('active')
        $(this).addClass('active')
        $('.footer').show()

        let file_list = self.getValidFileList(award)
        let file_total = file_list.length
        let photo_num = (award === 's1' || award === 's2') ? 1 : 40
        if (award !== 's1' && award !== 's2') {
          file_total = file_list.length - 1
        }
        photo_num = file_total < photo_num ? file_total : photo_num
        let award_num = typeMap[award].total - typeMap[award].take_num
        let singleNum = typeMap[award].single_num
        self.setState({
          award,
          file_list,
          file_total,
          photo_num,
          award_num: award_num > singleNum ? singleNum : award_num,
          photos: [],
          awardMan: null
        })
        self.getPhotoData()
        self.render()
      })

      //关闭弹窗
      $('.pop-up-close').click(function () {
        const { award } = self.state
        console.log(award)
        if (award != 's1' && award != 's2') {
          self.reRender()
        } else {
          $('.pop-up').hide()
          $('.pop-up .pop-up-content').hide()
        }
      })

      $('.galleryWrap').click(function (e) {
        let target = e.target;
        if ($(target).hasClass('person_image')) {
          let ind = $(target).data('index');
          console.log(ind)
          let url = self.getPhoto(ind)
          $('#gallery-one .item').each(function (index, ele) {
            $(ele).find('.item_a').css({
              backgroundImage: `url('${url}')`
            })
            $(ele).removeClass('active')
            // console.log($(ele).find('.item_a'))
          })
          self.setState({
            awardMan: ind
          })
          $('#gallery-one .item')[0].classList.add('active');
        }
      })
    }
    getWinnerByActive = (award) => {
      let { awardFileMap, awardMan } = this.state
      let items = awardFileMap['award' + award]
      let win = $('#gallery-one .active').data('win')
      if (win) {
        return [awardMan]
      }
      return []
    }
    startRun = () => {
      let i = 1;
      this.timer_td = setInterval(() => {
        if (i > 24) {
          i = 1;
        }
        $('#gallery-one .item').removeClass('active');
        $(`#gallery-one .t${i}`).addClass('active');
        i++;
      }, 30);
    }
    stopRun = (award) => {
      if (this.timer_td) {
        clearInterval(this.timer_td);
        let isWin = $('#gallery-one .active').data('win');
      }
    }

    /**
     * 设置奖项
     */
    setWinner = (award) => {
      if (award !== null) {
        this.setState({
          award
        })
        $('.cirle-btn').removeClass('active')
        $(`#award-${award}`).addClass('active')
      }
    }

    /**
     * 清除样式
     */
    clearStyle = () => {
      // 清除图片样式
      $('#gallery li.focus').removeClass('focus hover')
      // 关闭弹窗
      $('.pop-up').hide()
      $('.pop-up .pop-up-content').hide()
    }

    /**
     * 清除历史奖项
     */
    clearWinner = () => {
      this.clearStyle()

      if (!this.state.photos.length) {
        return false
      }

      // 图片重新渲染
      this.setState({
        photos: []
      })
      this.getPhotoData()
      const { photos } = this.state

      // 图片渲染
      // console.log('重新渲染图片', photos)

      $('#gallery li').each((index, item) => {
        let photo = photos[index]
        if (photo === undefined) {
          $(item).remove() // 缺少图片删除
        } else {
          $(item)
            .removeClass('animated bounce')
            .find('a')
            .attr('style', `background-image: url('${this.getPhoto(photo)}')`)
        }
      })
    }

    /**
     * 获取中奖者
     */
    getWinner = () => {
      const { award, photos, award_num, typeMap } = this.state

      if (award !== null && photos) {
        // 获取中奖人数
        // let count = this.winnerNumber[award]
        let count = typeMap[award].total
        let takeNum = typeMap[award].take_num
        let num = count - takeNum;
        let awardNum = award_num > num ? num : award_num

        let winners = []
        if (award === 's1' || award === 's2') {
          winners = this.getWinnerByActive(award)
        } else if (photos.length <= awardNum) { // 图片数量小于或等于中奖数，显示所有图片
          winners = photos
        } else {
          winners = this.getRandomArrayElements(photos, awardNum)
        }

        typeMap[award].take_num += winners.length;

        this.showWinning(award, winners)
        this.updatePhotoList(award, winners)
      } else { // 演示使用
        let rendomLi = this.random(this.state.photo_num) // 随机单个中奖下标
        $(`#gallery li:eq(${rendomLi})`).addClass('focus hover')
      }
    }

    /**
     * 显示中奖
     * @param award 当前奖项
     * @param winners 中奖名单
     */
    showWinning = (award, winners) => {
      const { file_list, awardFileMap } = this.state
      if (award == 's1' || award == 's2') {
        if (winners.length < 1) {
          $('#prize-no').show();
          $('.pop-up').show()
          return
        }
      }
      if (award !== null && winners && winners.length) {
        let group = $(`.prize-${award} ul`)[0]
        group.innerHTML = '' // 清除
        let winnerInfos = []
        winners.forEach(index => {
          let item = file_list[index]
          if (item) {
            winnerInfos.push(item) // 记录中奖者信息
            let number = document.createElement('div'),
                name = document.createElement('div'),
                photo = document.createElement('div'),
                img = document.createElement('img'),
                li = document.createElement('li')

            number.innerText = item.code
            number.className = 'user-number'
            name.innerText = `·${item.c_name}·`
            name.className = 'user-name'
            photo.className = 'user-photo'
            img.src = item.url.replace(/^\//, '')
            li.className = 'user-box'

            photo.appendChild(img)
            li.appendChild(photo)
            li.appendChild(name)
            li.appendChild(number)

            group.appendChild(li)
          }
        })
        console.log(award, group)
        $(`.prize-${award}`).show()
        $('.pop-up').show()

        this.saveWinnerInfo(award, winnerInfos)
        console.info(`${award}等奖名单:`, winnerInfos)
      }
    }

    /**
     * 初始化
     */
    init = () => {
      this.fetchPhotoList(() => {
        // this.getPhotoData()
        this.renderButton()
        // this.render()
        this.event()
      })
    }
  }

  const lottery = new Lottery()
  lottery.init()
})()
