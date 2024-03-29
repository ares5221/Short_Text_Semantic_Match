#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import json
import os
import csv
import xlrd

sentences_ann_dict = {'老师们，我在一线的时候总有一个问题，如何能够提高小组讨论的有效性？！如何避免讨论后小组派代表没人愿意说？或者一讨论学生们就聊别的这一问题呢？': 0, '怎样提高学生上课注意力？': 18,
                      '哪些班级特色活动让孩子感受到班级的温暖？': 0, '学生不交作业怎么办？': 17, '暑假回来上课孩子精力不集中怎么办？': 18, '如何发挥班干部的作用在班级管理中？': 0,
                      '学生不想上学，出现了厌学的状态怎么办？': 17, '学生谈恋爱怎么引导？': 23, '如何不让孩子们在百度作业帮上查答案？': 0, '学生沉迷游戏怎么办？': 22,
                      '如何安抚考生成绩不理想？': 0, '怎么让孩子喜欢哲学？': 0, '学生上课爱睡觉怎么办？': 4,
                      '学生遇到一点小事情就爱发脾气，一有点不顺心就哭，总是觉得大家应该围着他转，如何帮助孩子学会控制情绪？': 14,
                      '怎样学好英语？有什么学英语的还办法？我是一个文盲妈妈，我的孩子刚升三年级的学生。': 0, '课堂上怎样做才能提高课堂学习效果？': 0,
                      '怎样能教好一年级的语文拼音，尤其是带调拼读音节。班里的学生看着声调读出来的确实另一个调。': 0,
                      '如何让家长多辅导学生完成作业，尤其是在遇到作业中的难点时，能适当的给予学生指导？最近一篇《陪娃写作业？算了吧，想来想去还是命重要》的文章刷爆了朋友圈，很多家长认为陪娃写作业，就像下凡历劫。': 0,
                      '怎样引导发现孩子的闪光点？': 0, '学生不爱写作业该怎么办？': 17, '老师该怎么检查学生作业呢？委托组长检查效果不佳。': 0, '课堂上学生对我讲的内容提出质疑怎么办？': 3,
                      '二年级有几个孩子真的特别捣乱，一直扰乱课堂纪律怎么办？': 5, '如何让小学生喜欢上美术课？': 0, '上课总是说话怎么办？': 5, '如何面对学生不按时完成作业的问题？': 17,
                      '怎么培养孩子的阅读习惯，激发孩子的阅读兴趣呢?': 0, '学生不写作业怎么办？不做作业，不交作业怎么办？': 17, '如何给低段孩子开展阅读教学': 0,
                      '面对形形色色的问题学生，该如何转化教育？': 0, '如何培养学生的数学思维能力？': 0, '对于每个孩子的闪光点，如何因势导利？': 0,
                      '现在的学生学习主动性差，老师需要想方设法的来调动学生学习的兴趣？如何让学生以饱满的热情参加学习，真正提高学习主动性？': 17, '参加辩论有什么好处？辩论时需要教师提前做什么准备？': 0,
                      '五年级的孩子，基础只有二年级学生的知识，这个怎么办？': 16, '怎么样可以上好音乐课？学生不愿意学习乐理知识，不喜欢上欣赏课怎么办？': 17, '如何布置有效的数学作业？': 0,
                      '老师如何布置即有效又有趣的家庭作业呢？': 0, '为什么现在的学生越来越被动学习？': 17, '如何调动孩子的学习兴趣？': 17, '怎样有效提高教学水平？': 0,
                      '对班级里的学困生怎样进行辅导？': 0, '学生写字的姿态如何教正？': 0, '对于九年级学生的厌学情绪，有什么好方法解决或激励学生？': 17, '如何提高教师的课堂管理能力？': 0,
                      '有些孩子基础太差，该如何提高他们的成绩？': 16, '孩子胆子小怎么办': 12, '如何在常规教学中培养尖子生？': 0, '偏科怎么办？学生出现偏科的现象怎么处理呢？': 16,
                      '遇到精神有问题的学生怎么办？': 0, '如何培养孩子的预习习惯?': 16, '对学习不感兴趣，对待考试态度不端正的学生我们如何怎样引导？': 17,
                      '孩子学习没兴趣，怎样让被动学习变为主动学习？': 17, '如何开发语文课程资源': 0, '一线语文教师，如何引导学生“多读书，好读书，读好书，读整本书”呢？': 0,
                      '怎样让一年级新生在音乐课上学会识谱': 0,
                      '我们学校一直在进行课程评价改革，期中语文考试取消了试卷答题的形式，而是测评同读一本读书、课文古诗词背诵情况、写字、演讲等几种。数学进行计算测试和算理面试。语文评价大步向前，数学评价却放不开，请问各位同事，在数学评价上有什么创新的评价方案吗？': 0,
                      '小学六年级的学生，对于老师的批评教育总是抱着无所谓的态度，有什么更好的办法引导学生？': 3,
                      '我是一名小学科学教师，我想问一问有关科学实验中实验记录的问题，我个人觉得这个实验记录是个“鸡肋”，在课堂上写完的话会耽误很多时间，影响本课教学进度，而且部分学生还完成不了。如果不完成的话“上面，上上面”还做未一个项目要检查，来了之后还会找到好~~~多问题，字写得不好，表格设计不合理……，大家是怎样对待实验记录的？好方法分享一下啊！': 0,
                      '高中孩子缺乏学习热情怎么办？': 17, '有什么好的方法让学生喜欢你，并且特别听你的话？': 0, '怎样挽救学习不好的学生？': 0, '做为一个老师如何更好的和青春期的孩子相处？': 0,
                      '在同一节课上，优等生总是迅速完成学习任务，甚至再布置的高难任务都完成了，而学困生只是完成一点点，此时该让优等生做些什么呢？': 0,
                      '遇到不配合教学的家长，你会怎样处理？有哪些方法促进老师与家长建立良好的关系?': 0,
                      '现在课堂上不允许体罚学生，请问如何让纪律不好的学生安静的听课，我试过奖励、表扬、软硬兼施，似乎没什么效果，求好的方法！': 5,
                      '对于淘气好动的学生，你采取的什么对策呢？是惩罚？是说教？还是征服？': 5,
                      '老师们，我对一年级数学绘本教学很有兴趣，可是不知道数学绘本具体怎么操作，绘本课怎么上的，想请老师们推荐些案例学习，教教我怎么实施。': 0,
                      '自主阅读时，有点孩子读进去了，能够自己发现问题进而解决问题，可有些孩子似乎在看热闹，对于这部分学生我们该怎么办呢？': 17, '怎样提升老师的内生动力': 0,
                      '怎样持续保持低年级孩子注意力呢？': 18, '如何做好小学班主任团队建设？': 0, '请问对缺乏家庭关爱的孩子如何提高她的学习兴趣？': 17,
                      '如何提高一年级学生运用拼音的能力？': 16, '体育课余训练中，家长不支持，如何与家人沟通': 0, '怎样提高学生的逻辑思维能力？': 0,
                      '如何协调优等生和学困生在同一节课完成相同作业的时间。': 0, '怎样让后进生喜欢上学习？': 17, '如何避免五年级孩子过多依赖作业帮等软件完成作业？': 16,
                      '怎样让学生养成良好的行为习惯？': 0, '班主任如何让“问题学生不再问题”？': 0, '老师们，在数学课堂如何更好做到让学生不接下句？': 0,
                      '如何让家长们意识到家庭教育在小学教育中的重要作用？': 0, '在教学中有哪些有助于能力培养的教学方法和策略？': 0,
                      '怎么才能有效提高后进生的成绩呢？小学高年组英语在期末复习阶段，学习成绩好的同学依然好，可后进生却没有提高，非常影响班里的整体成绩，': 16, '如何改变学差生的学习态度?': 17,
                      '班里有一学生总喜欢拿别人的东西，多次说教无济于事。近些时候竟然把老师说教科书写上自己的名字，已两次了。咋办？': 8, '怎样提高孩子的作文水平？': 16,
                      '班级里孩子学习的速度参差不齐，我们如何开展学习，使每一个孩子都不掉队？': 0,
                      '我的女儿甜甜今年上小学六年级了，平时话不多，性格有点内向，总是不想去学校，每天回家都闷闷不乐，我问她发生了什么他也不说。有一次，我发现她躲在屋子里偷偷抹眼泪，我问她到底怎么了。她告诉我同桌欺负她，她又不敢告诉老师。\n我从老师那了解到，甜甜上课从来不敢举手回答问题，就算老师点名叫她回答，她也不敢张口，半天说不出一句话，有时甚至会急哭。': 11,
                      '怎样平衡体育训练和文化课程之间的矛盾': 0, '六年级的孩子们开始早恋，写情书，学习成绩下降，大家有什么好办法？': 23, '如何关爱留守学生？': 0,
                      '学生很喜欢和老师聊天，但是所有的问题都和学习没有关系，教师怎么把学生这份聊天的热情引导到学习上呢？': 0,
                      '现在的家长总是对老师的工作指手画脚，安排值日怕孩子累着，拍个球嫌孩子衣服脏了，甚至有家长把老师当做保姆，吃药的事情都让老师代劳。遇到这样的家长怎么和他们沟通呢？': 0,
                      '老师们，如何合理安排学生座位呢，班主任经常接到家长电话要求将孩子排在前面来该怎么办呢。': 0,
                      '最近出现家长在孩子作业上留言"老师晚上好，以后批改作业请认真点!"此事引发闷络热议!你怎幺看?': 0,
                      '学生家长因为自身素质问题，不能够胜任辅导学生的学习任务和习惯养成，以至于学生在家庭的学习效果很不理想。我该怎么做呢？': 0, '学生如何高效的利用学校时间？具体该怎么做呢？': 17,
                      '怎样实施差异性教学？': 0, '如何教好信息理论课？': 0, '美术课上教师展示示范作品后，很多孩子绘画或制作与老师雷同的作品，没有创新，如何让学生发散思维创作新颖的作品呢？': 0,
                      '九月我接三4班。班里有个孩子弱智同时患有癫痫病，在校的活动必须有人帮助才能完成（她妈妈一直在陪读），其二班里还有一个多动症的孩子：在学校的一天里会无休止的画，撕，课堂作业基本不写，逼得紧了就动笔画一画，学校集会他从来不会安静的站立，总是无休止的闹，其三还有一个大脑工作能力差，从来不会课堂听讲，随堂测：英语0语数0-30分徘徊。我该怎么有效的辅导他们？': 0,
                      '怎样让学生提分快？': 0,
                      '对于不听话、叛逆的孩子，该怎样和他相处？王老师：小明，把作业交出来！小明：没带！王老师：小明，上课不要讲话，不要影响别的同学学习！小明：（安静3秒钟又开始捣乱）王老师：小明，老师跟你讲什么你都听不进去！（已崩溃）小明为什么会这样呢？孩子在学校里的叛逆行为可能有：与老师同学争吵打架；逃课；不做不交作业；上课不听捣乱；不愿意参加集体活动；上学情绪低落；与家长顶嘴，唱反调。': 5,
                      '教学为什么提倡创设情境': 0, '有什么提高学困生学习成绩的有效方法吗？': 16,
                      '班里有个孩子让家里人娇惯的没一点儿规矩，站没站相，坐没坐相。课堂上不遵守纪律，老师警告一句就哭得稀里哗啦的，不知道情况的人还以为老师怎么他了。父母不以为然，总是让老师多管管。沟通几次，效果不好。怎么办呢？': 5,
                      '怎样让孩子的基础更扎实呢？给孩子听写的过程中发现，多次强调的字词还是写不对，有的这次写对了，下次依旧错。默写的诗句则是添字漏字换字。怎样提高孩子的听写正确率呢？': 18,
                      '怎样能让没有毅力的孩子坚持学习呢？': 17, '如何开展班级活动可以提高学生核心素养？': 0, '如何对待不完成作业的孩子？': 17, '如何解决学生作文内容类似的问题？': 0,
                      '怎么样才能让学生学会拼音？无论怎么教，还是有一部分学生不会拼拼音.': 0, '期末复习怎样做到高效': 0, '如果学生没有在规定的时间内完成背诵任务，有什么好的方法解决吗？': 16,
                      '如何让孩子学会感恩？孩子太自私，不懂感恩，怎么培养？': 21, '期末该怎样来合理的复习呢？': 16, '假期如何督促学生学习？': 0,
                      '期末复习期间，学生大致会出现以下三种现象：现象一，感到焦虑，不知道该怎么复习，常常“眉毛胡子一把抓”，或者“捡了芝麻，丢了西瓜”。现象二，老师带着复习也不愿意复习，回家只是“磨洋工”。现象三，心态不好，担心万一考砸被父母批评，心里阴影重。要想考试不掉链子，您会怎样帮助学生调整心态，积极迎考？': 16,
                      '现在的学生自觉性很差，听课的注意力更不集中，如何能改善这一点？': 18, '孩子上课总睡觉怎么办？': 4,
                      '小学六年级的学生对老师发布的任务置若罔闻，还干扰其他学生完成，不停的说些与课堂教学无关的话，与之沟通东拉西扯，哪位同仁有解决此类问题的高招？': 5,
                      '对于九年级的学困生，厌学是显著特征。任凭你老师找来家长陪读或是软硬兼施，让他看看书，写写字，各种招数，就是不学，考试一字不答。如何处之？': 17,
                      '如何让孩子正确认识自己，提高学习兴趣？': 17, '如何上好复习课?': 0, '复习了一段时间，怎么发现，问题越来越多，怎么办？': 0, '孩子复习进不了状态怎么办？': 17,
                      '如何帮助后进生？': 0, '现在的孩子缺乏感恩，多数以自我为中心，情感缺失怎么办？': 21, '如何让学生对写作文感兴趣，怎样才能写好作文我有些困惑。': 17,
                      '学生的计算能力总是提不上去，现在的孩子为什么总是那么浮躁，沉稳的没几个。': 16, '如何能让孩子学会感恩？': 21, '教室要如何做才能从本质上改变后进生的学习态度？': 17,
                      '如何跟学生讲清联想和想象？': 0, '九年级的女学生，天天上课沉醉在自我化妆上，上课中不是化妆照镜子就是睡觉，有点目中无人，自我为中心，该怎么说教？': 6,
                      '对于学生说谎该怎么处理更合适？今天是周末，我们班上有几个孩子自己约着去同学家玩，还哄骗家长说是我要带他们出去聚会，结果家长信以为真，最后打电话给我，我说我在老家，根本就没这回事，家长才知道被骗了。': 7,
                      '如何引导粗心大意的学生？学生在做计算题时，计算方法没有问题，但总是将数字看错，比如说题目上写15，他做的时候就变成5了。': 18,
                      '寒假将至，假期可以安排哪些作业？既做到减轻孩子的负担，又可以让他们度过一个有意义有收获的假期？': 0, '面对学生在期末复习过程中出现的倦怠现象，您会采取哪些做法？': 0,
                      '班上的学困生怎么努力都没效，有好的方法吗？': 16, '怎么培养学生对学习的积极性？': 17, '怎样对待性格极内向的单亲孩子？': 0,
                      '怎么解决早恋问题？我们班的同学建立了一个追女生的群，懵懂中有早恋的现象！': 23, '期末复习过程中怎样防止学生复习倦怠呢？': 16,
                      '如何布置寒假作业，即减轻孩子的负担，又让他们度过一个有收获的假期？实践性寒假作业：打球跳绳，跟家长一起贴春联，每天坚持体育锻炼、课外阅读。游戏式寒假作业：重庆清华中学学生的寒假作业是玩网游《化学加油站》。该游戏共35关，由该校化学组老师设计。\xa0体验式寒假作业：重庆南岸区黄桷垭小学让学生抽扑克牌。赵伊湄抽到了“红桃2”，作业是在一个月内不碰手机和电脑，用阅读和与同学互动代替。': 0,
                      '如何培养学生写作的兴趣？': 17, '假期如何监管？避免孩子过度使用电子产品如电视、电脑、手机、平板等。': 0,
                      '如何帮助孩子过渡小升初的阶段？小学升入初中，学科增多了，作业量也增大了，很多同学感到无所适从。': 0, '对于无法与家长进行亲子活动，完成老师所留的一些家庭作业的学生该怎么办？': 0,
                      '面对离异家庭的单亲学生应该怎么办？': 0, '小学生如何学好英语？家长不管或者不知道如何辅导？': 16, '如何能快速的形成班级凝聚力？': 0, '如何布置高质量的英语寒假作业？': 0,
                      '当遇到屡教不改的学生时应该怎么办？': 20,
                      '班里有个孩子反应有些慢，学习上有点儿困难，和家长交流过，老师建议她在家耐心辅导。家长不会辅导，总是隔三差五地在晚上给老师打电话，老师把好的方法建议教给她，并告诉她别急慢慢来，孩子慢慢会进步的。可这位心急的妈妈总是问，俺儿是不是倒数第一啊？她愁死了。作为老师和妈妈，在晚上也要辅导自己的孩子，也有很多家务事要做，总是这样被家长打扰，也是很苦恼。': 16,
                      '期未复习课时由于两极分化严重，优秀生“吃不饱”而潜能生“吃不下”怎么有效平衡呢？': 0, '怎样布置有效果的小学寒假作业？': 0, '如何让孩子爱上阅读？': 0,
                      '如何做好留守儿童的思想教育？': 0, '如何让高中生远离游戏，爱上学习？': 22, '如何让学生自觉执行制定好的假期计划？学生制定假期计划，书面上很合理，执行起来还是要靠监督。': 0,
                      '老师备案除了知识点，最需要考虑的是什么': 0, '如何帮助学习困难生？就是那种听不懂授课内容考试几乎是个位数的学生？': 0,
                      '孩子聪明，但课堂上不听，作业不写，扰乱周围学生，课下打架惹事，家长护子心切，从不说孩子的错，对不写作业置若罔闻。咋办？': 17,
                      '孩子平时写作业还行，就是一到考试就考不好，尤其是数学，请问怎么办？': 16, '沟通怎样做': 0, '班里孩子两极分化厉害，怎么帮助班里的好多差生提成绩？': 16,
                      '怎样合理的安排孩子的假期作业呢？': 0, '有什么好方法让学生爱上阅读呢？': 0, '怎样才能让孩子自觉做作业呀？': 17, '不守信用的孩子怎么教育？': 9,
                      '儿子已经上三年级了，可是吃饭总是一个大问题，为此我用尽了一切办法，曾经有过罚他一天不吃饭的记录，可是伤还没好就忘了痛。没办法不得不拿起碗筷把饭菜送到他的嘴里。作为老师我却没有办法教育自己的孩子，真是个烧脑的大问题？怎样才能解决呢？请高人指条明路？': 0,
                      '假期里怎样让孩子爱上阅读？': 0, '如何让孩子学会控制情绪？班里有个控制不住情绪的孩子，如果老师和同学不满足他，他就哭闹，影响上课。': 5,
                      '马上开学了，如何让学生快速适应紧张的学习生活！': 0, '孩子不爱写作业怎么办？': 17, '八岁的孩子注意力不集中怎么办？如何培养一个八岁孩子的注意力，上课总溜号': 18,
                      '留守儿童的家教缺失，厌学甚至想辍学该怎么办？': 17, '我所教的学生都是维吾尔族小朋友，家长大部分不会汉语，不能给孩子辅导，这样的大背景下，我该如何教育孩子？': 0,
                      '我是初二的班主任老师，班级学生总说话，该怎样在短时间内解决这个问题？': 5, '如何改变孩子磨蹭的不好习惯': 0,
                      '如何帮助留守学生？陈佳同学（化名），四年级单亲留守女生。（该生学前教育为零，一年级仅上一个月就随父外出打工，打工外期间辍学，二年级第一学学期期末回到本班学习。）该生语文各方面能力都很差，是一名学困生。课上我经常关注她，课下也经常对她进行辅导，让她多读多写，希望等提高她各方面的能力，可是收效甚微，请问对这样的学生我该怎么办？': 0,
                      '有一些学困生,他们的阅读量主要是课内阅读，课外阅读几乎为零。没有阅读量的孩子，如何阅读理解，更何谈习作与积累，没有积累怎么写，写什么？我观察，对于这部分孩子来说，有了习作范例，似乎也算是在课堂上的一点儿积累了。通过读范文，结合自己的生活实际，仿照写出属于自己的作文。时间久了，学困生也不至于一写作就放挺了。基于这种情况，我想建议，能否在每单元习作后附一些好的习作，供学困生阅读？': 0,
                      '当孩子沉迷手机游戏时，应该怎样有效沟通？': 22,
                      '如何帮助单亲家庭的孩子？女生，五年级。数学、语文成绩，在班级是下等。母亲打工维持生活。家庭作业经常完不成。收作业时就说忘带了，和家长打电话沟通，家长说没有写。家长反映，在家没有妈妈监督作业就少写，这学期开学家长督促也不写。在平时的教学中，我也经常采用表扬、奖励、贴小红花、谈心等方式来帮助她。当天她也挺开心，表现也很积极，但过后收效甚微。几天后又犯老毛病': 0,
                      '怎样提高学生的写作技巧呢？平时学生在习作中，我总是“抓两头，补中间”可这样下来学生文章篇幅短小，容易出现千篇一律，学生写作有很大局限性。': 16,
                      '孩子很懒不按时完成作业怎么办？班上有个男孩，很聪明，成绩还可以，但是特懒惰，不能按时完成作业，我多次找他谈话，但是效果不是很好。': 17,
                      '我们班有个同学特别好动，上课注意力不集中，在家里写作业也能磨蹭，我和他的家长采取了很多方法都没有成效，针对这样的学生该怎么办？': 18,
                      '如何让家长督促孩子多读课外书？提高孩子阅读量，从一年级入学以来，一直多次跟家长强调读书的重要性，也经常在班级用各种方式鼓励孩子多读书，例如读书卡，读书笔记完成的较好的，阅读方面进步大的同学进行物质鼓励和精神表扬。但是班级仍有将近三分之一的孩子在课外阅读上毫无起色，家长在亲子阅读上也不是很配合，日积月累下来，语文成绩的两极分化越来越严重！': 0,
                      '学生总是违反课堂纪律，对待学习多态度散漫，上课总是说话，不是前后桌说话，就自言自语，': 5, '老师我家孩子三年级孩子反映慢，学习不好我想让他留级可以吗？': 0,
                      '教师如何引领学生读一整本书': 0, '对于早恋应如何进行合适的教育引导？': 23,
                      '怎样才能让熊孩子们按时完成作业？对班里的一些熊孩子不按时交作业，经常不交作业，甚至是不写作业。到底怎样才能让熊孩子按时完成作业，积极提交作业？': 17,
                      '如何更好地了解留守儿童，单亲家庭的孩子的心理动态？': 0,
                      '班级有这样一个女孩子，她性格开朗、待人热情，但就是注意力特别难以集中，平时和她交谈一个话题，不到三句就开始跑题。课堂上，她不是处于找学习物品的状态中，就是陷入一种傻傻发呆的状态里，控制不住两只爱摆弄的小手，控制不住抢答老师的提问，可总是答不对，且错得很离谱。一到课堂作业环节，她总是会问老师或同学用什么本怎么写……我和家长想了很多办法都是收效见微，希望专家老师给予我解决此类问题的方法，谢谢！': 18,
                      '小学作文教学一直都是教学中的难点。我班杨微、马华、生音都是单亲、留守儿童，见的世面比较少，平时也不爱读书，爷爷、奶奶没文化，有的因为是单亲，家长对孩子特别溺爱，不配合老师，不能在家督促孩子完成作业，读课外书，导致孩子作文空洞，素材不新颖，语言贫乏，语句不通顺。尽管我在教学中引导他们用心观察生活，写日记，读课外书，积累好词佳句，针对他们出现的问题进行个别指导，但收效甚微。我也不知怎么办？恳请各位专家': 0,
                      '班级里的后进生，我坚持每天辅导，可是成绩提升的效果不明显，那么怎样调动学生的学习积极性呢？这样做效果好吗？': 17, '老师们，对于班上经常不完成作业的孩子，你们有什么好办法？': 17,
                      '怎么教育个性很强的女生？班里有个女生非常的有个性，很会顶嘴还嘴，能把人气个半死，对于这样的学生，该怎么教她呢？': 2,
                      '我们班有个孩子，就喜欢满教室到处跑，他家市场卖菜的，跑习惯了，跟他说不要在教室跑听话，管不了1秒钟，抓也抓不住，话多的没办法，别的孩子都在学时，他也到处跑，要么去玩积木，要么去玩其他的，让他好好学，他就不听，只往地上坐或者使劲挣脱老师又跑走了，还喜欢动手打人，思想工作没办法做，把我们班孩子都带动的特别的躁动，怎么办呢？他家家长也是说他根本坐不住，管不了': 5,
                      '怎么样让学生在课堂合作学习中发挥最佳效果？': 0, '因为老师没收手机，孩子离家出走，对于任性不服管教的学生，老师该怎么办？': 24, '如何开展优秀的班级文建设?': 0,
                      '在家庭关系破裂等不和谐环境中成长的孩子，我们到底应该怎样帮助和教育他们？': 0, '孩子们上课爱讲小话，上课说话怎么办？': 5, '如何让孩子爱学习？': 17,
                      '夏天孩子们因为燥热，注意力不集中听课怎么办？': 18, '孩子不喜欢学习，对写作业不积极，非常怕读书写字的，怎么样才能让孩子爱上学习。': 17,
                      '核心素养如何基于校本在学科整合中落地？': 0, '如何激发孩子们读书的兴趣？': 0, '如何让孩子远离手机，爱上学习？': 22, '怎么在短时期内挽救一个厌学的孩子?': 17,
                      '怎样让孩子能既喜欢你，又害怕你？': 0, '学生的课本作业本来到教室后经常丢失怎么办？': 0, '针对智商高但不爱写作业这样的孩子怎样教育？': 17,
                      '有这样一种孩子，把什么都看得很淡漠，没了自尊，到底是受什么影响呢?': 0, '怎样引导思想包袱重的孩子？': 0, '如何促进班上动作慢悠悠的孩子？': 0,
                      '班主任罗健遇到了这样一些家长：“我不识字，教不了孩子。”“搞什么亲子阅读，我没时间。”“孩子不听我的，让我怎么办。”这些孩子存在不守纪律、学习态度不端正、厌学等等状况。罗健操碎了心，微信群、电话、家访、约谈，什么形式都用了，收效甚微！\n孩子的教育需要学校与家庭相互配合，你存在同样的烦恼吗？在和家长沟通时你有哪些沟通策略和技巧？': 0,
                      '各位老师，我们家孩子现在一年级，上课不听讲，总是自己在那写写画画的，还总是出声音，老师提醒他，他还发脾气，不听老师的劝，总是爱发脾气，还总和同学发生冲突，分不清闹着玩还是认真的': 5,
                      '为啥孩子既不爱学习，对成绩也不在乎？': 0,
                      '我的儿子现在四年级，最近都不愿意写作业，开学的时候还是很积极的，当天的作业做完以后还想把第二天的做点掉，可最近一段时间做作业拖拖拉拉，周末都要拖到最后一天的晚上才去做，遇到作文就不想写，还搞得很委屈，流眼泪，真不知道该怎么办才好！': 17,
                      '孩子写作业不认真，有什么办法让他能认真坐下写作业？': 17, '如何提高学生在数学课上的表达能力？': 0, '课堂沉闷，学生没有兴趣，如何激活课堂、激发学习兴趣？': 17,
                      '如何提高小学生汉语口头表达能力呢？': 0, '学生怎么合理安排课余学习时间？': 16,
                      '罗健老师班里就有这样的孩子，章奇因为数学成绩总是不佳而不自信；李梅梅因为身材矮胖，总是怕同学嘲笑她；曾晓家里贫困不喜欢与同学交往……如何培养一个自信的孩子，对于不自信的孩子应该怎么鼓励？': 0,
                      '孩子上一年级，我家孩子比同学小一岁，原来有两个好朋友玩的很好，现在两个朋友都不跟我女儿我玩了，还说她坏话，她很困惑，该怎样开导她': 0,
                      '对于经常不完成家庭作业的孩子，老师们有什么好的建议吗？': 17, '孩子上课总是不听讲 专心自己的事情 如何帮助改正呢？': 18,
                      '要开家长会了，总感觉家长会对部分家长来说没有什么意义，总感觉不配合教师工作，求支招': 0, '如何转化后进生？': 0,
                      '怎样让孩子养成良好的学习习惯？上课不听，下课疯玩，放学不写作业……什么都喜欢，就是不爱学习。坐在书桌前就犯困，吃饭一餐不落下。学习已经成为终身的行为，从小培养孩子的学习自觉性十分必要。怎样让学习像吃饭睡觉一样，成为一种习惯？': 17,
                      '孩子爱写作业的动力培养': 17, '如何培养学生良好的思想品质和行为习惯？': 0,
                      '写字犹如人的第二张脸，可见写字的重要性，但是现在每天都在紧张的忙碌着，孩子们写字时就有些心不在焉，怎样能让孩子们养成“动笔就是练字时”的好习惯呢？': 16,
                      '孩子接受能力慢，别的孩子一讲就会了，我家孩子的学好几次才能理解，没次放假就得把下学期的学一遍，要不开学跟不上，这才上小学，等上初中和高中该可怎么办？谢谢！': 16,
                      '孩子学数学没信心很吃力，你说她不会又会，但是经过转校后，分数下降厉害，真是没招～': 0, '怎样培养孩子的良好学习习惯': 16, '如何处理两极分化': 0,
                      '孩子作文写不具体怎么办啊？': 16, '如何培养学生自主管理能力': 0,
                      '班级里的孩子成绩差异大两极分化该怎么办？班级里的孩子成绩有好有坏，入学时都差不多，到了中高年级差距不断拉大，出现两极分化。\xa0教学进度稍微快点，有些孩子跟不上；照顾到部分孩子，成绩好的孩子觉得没意思。': 0,
                      '数学教学中如何调动学困生的积极性？': 0,
                      '在教学管理中，有一个学习较好的学生，但却非常自私自利，在今天下午班级大扫除时，作为班长的她，自己一个人坐在座位上学习，我非常生气，但因为马上中考，我又忍住没发火，各位同事，你们如果遇到这样的情况，该怎样处理？': 21,
                      '请问如何有效纠正孩子上课注意力不集中，爱做小动作爱讲话的坏习惯?': 18,
                      '我班小A同学，回答问题没声音，上课总是低着头，就连做操也做不到位，全体同学朗诵时也是不张嘴，是不是缺乏自信呀，我们怎么帮助孩子呢？': 0, '怎样改掉学生做事拖拖拉垃的坏习惯': 0,
                      '如何处理学生偷窃行为？橡皮丢了，铅笔没了，课本不知道哪去了……由于低年级学生自控能力较弱，道德发展水平尚未健全，“偷窃”行为在学校内时有发生。于学生这种不良行为，作为老师到底应该怎样处理？': 8,
                      '学生不小心磕伤，其爷爷、奶奶、爸爸、妈妈齐到校兴师问罪，应怎样处理较合适?': 0,
                      '我班（小学六年级）一学生经常不做作业，一再提醒他完成，可他说，昨天晚上他爸爸守着做了，今天忘带了……我重新给了他一份作业，可他磨磨蹭蹭，就是不做。语文课了，我只好离开教室，下来再找他…对于这样的学生，怎么办？': 17,
                      '今天一弱小的调皮生下课时哭了，我问他怎么了？他说：我不小心去摸田同学，可他就给我两下！其实，我明白，这孩子经常惹事生非，我于是对他说：老师天天在讲别招惹别人，你去惹别人，就得承受带来的打击??……（当然，私底下我会给另外一个孩子讲，同学间要友好…）不知道这样处理是否好': 1,
                      '如何引导孩子树立正确的人生观?': 0,
                      '班上一个男孩子(二年级)，头脑较灵活，但爱给他人取外号，爱说一些脏话、坏话，爱动手弄别人，不太受约束，比较自我，经过坚持不懈的学校教育和家校结合教育，有进步，但反复，请问怎么做？': 2,
                      '现在的一年级孩子，在和别人玩耍中受伤，总是和家长一起把所有责任都推给别人，而且一旦受伤，好像任何人都是他的敌人。大家怎么处理，教育的？': 0,
                      '大家可以谈谈学生发展核心素养对我们教师提出了什么新的要求吗？谢谢': 0,
                      '我班有一个女生（六年级），数学课上她身体总是这里那里的不舒服，一会儿吵头痛，一huier肚子疼……学习自然就不好。可是，一说到跳舞，学校开展的文艺活动，她却如鱼得水，而且跳得特别好！（我经常请她领舞，也常常跟着她跳课间舞）一天，她课堂上又趴在桌子上，我说：你像跳舞那样对待学习！道理讲理一箩筐，家长也常联系，沟通，可是收效甚微！\n        请大家帮忙出主意': 17,
                      '小学三年级，有这样一类学困生，课上捣乱，不学习，课下作业拖拉不交。找他们谈话总是闷不吭声。和家长沟通，家长也比较溺爱孩子，总是说在家也要求他写作业了。可是这样的孩子一点改变也没有。上课自制力很差。该不听还是不听。作为班主任也比较头疼，给他们自信心，又不能时时刻刻盯着？各位前辈们，这样的事情该如何是好？': 17,
                      '第10周问题：面对不同家长，你会如何见招拆招？你还遇到过什么样的家长？\n1. 放弃型：对孩子在校表现不闻不问，认为教育是老师的事。\xa02. 冲动型：孩子在学校出现状况时，马上找老师兴师问罪。3. 依赖型：缺少主见，教育孩子时遇到一点问题，总是找老师解决。4. 多疑型：对老师缺乏信任，在家多溺爱孩子，遇到问题总质疑老师。5. 焦虑型：孩子成绩稍有下降就无法接受，情绪易波动，抱怨孩子、抱怨老师。': 0,
                      '对于变相体罚，你是怎么理解的？': 0,
                      '说起家长，老师都感觉家长都在意味的忙于工作，不顾孩子，孩子送到了学校就应该是老师的事，与家长无关。其实有时间不是这样的，许多家长也想管孩子， 但是他真的不知道怎样合理的去抓，严厉批评教育，跟随监督都尝试了，孩子自己意识不到学习，家长处于无奈也会选择放弃，有时间真的不知道该怎么办了？老师也让顺其自然，这可怎么办？': 0,
                      '现如今，大多孩子都是独生子女，往往是爸爸妈妈爷爷奶奶四个人照顾一个孩子。当爸爸妈妈对孩子的教育和爷爷奶奶对孩子的教育发生分歧时怎么办？当孩子犯错需要惩罚时爷爷奶奶百般阻挠怎么办？爷爷奶奶明知惯子如杀子还是忍不住要溺爱。': 0,
                      '求助:孩子每次上课都要迟到几分钟，经我询问了解，原来是他教室门口的水龙头经常就坏了，为了不浪费水资源，他总是要最后一个离开那个水龙头。没关时，他一定要关住，水龙头坏了时，他要想办法修好。面对孩子节约能源的思想品质，我高兴他有关注节约能源的意识；面对课堂，面对老师，我觉得孩子自己坚持修理总是最后一个离开水房不是长久之计……\n问题:我该怎么做？孩子该怎么做？我该引导他怎么做？': 6,
                      '孩子厌学怎么办？': 17, '身边或媒体经常爆料一些教育的负面信息，很影响教师的情绪。作为学校管理者，除了对教师进行阳光心态引导，进行法制学习，开展活动舒缓压力外，还有哪些好的做法？': 0,
                      '为了进一步培养学生的自主管理和自我教育的能力，我校准备通过竞聘上岗的方式选拔一批优秀学生组建学生会，请问怎样有效指导初中生学生会干部开展工作？': 0,
                      '第11周问题：如何让传统文化走进课堂？（分享你的思考或者设计过的教学和活动）\n端午将至，软糯清香的各色粽子又开始争奇斗艳。端午节为什么要吃粽子？除了吃粽子还有哪些习俗？孩子们是否了解美味的粽子背后所隐藏的中国传统文化？\n中国传统文化博大精深，教师肩负着传承中华优秀传统文化的使命，如何巧妙地将其融入日常教学是每个老师需要思考的问题。': 0,
                      '一直都有家长托熟人找领导给老师说让多照顾孩子，让老师好好教育孩子在家也听家长的话。孩子在家任性，不听话，家长不是想办法去教育，而是埋怨老师教育不当，甚至找校长告状。家长们完全把孩子的教育推给学校、老师。': 0,
                      '现在孩子的阅读习惯好难养成，老师督促一下，他们读一下，不督促就没有课外阅读的习惯，。回家后家长也不积极引导，现在留守儿童比较多，爷爷奶奶、外公外婆根本就管不了，不是看电视，就是玩手机。一到写作时，语言贫乏，内容空洞，不能表达自己的真情实感。怎样让孩子们养成良好的阅读习惯呢？一直以来比较困惑。': 0,
                      '对于家长把孩子送到学校，从来不闻不问孩子作业情况，孩子在校表现出的任何情况，求支招！谢谢！': 0,
                      '我班有个学生做作业总是三心二意。一会儿抓氧，一会儿找笔，一会儿咬手指头，一会儿晃晃腿。据家长反映，该生在家写作业也是这样，一会儿喝水，一会儿小便。即便是要求该生在写作业之前完成这些琐事，但做作业途中仍然改不了这些坏习惯。应该怎样做才能帮助该生改掉这些坏习惯呢？': 18,
                      '教师心理健康的标准是什么？': 0,
                      '写评语是老师教学中不可缺少的一个环节。\n不是在写评语，就是在思考写什么评语。\n小到作业评价，大到期中、期末总结；它代表着教师对学生学习成果的反馈和对学生的期望。\n优秀的评语可以激励学生、帮助学生建立自信；不得体的评语反而会引发学生抵触、反感等负面情绪。': 0,
                      '一年级的学生经常会发生一些矛盾，每天告状的也很多。如果不管的话家长又说老师不管，管的话根本管不过来。有时候还会发生受伤时间，双方家长都不肯示弱。应该怎么办？': 1,
                      '如何做好毕业班班主任工作？': 0, '有一些人每逢考试就会出现焦虑、紧张、失眠等症状。作为老师，你该如何帮助学生消除考前恐惧？': 14,
                      '实际工作中总有一些学生，老师讲过的课对于他来说，就像没有听说过一样，是哪个环节出了问题？': 0, '为了让孩子的假期有意义有规律，暑假怎样提出要求才更容易让家长接受？': 0,
                      '如何发掘留守儿童的优势？留守儿童是当今学校教育中非常关注的一个特殊群体，其教育问题是学校所面临的现实而又亟待解决的难题。大多数教育者关注的是如何解决留守儿童出现的负面问题，却忽略了其优势的发掘。\n最有力量的教育是通过发掘儿童自身的优势资源进行引导的教育！': 0,
                      '我班有个男生，平时不多言，最近一段时间沉迷网络游戏，父母没收了手机之后，又攒钱买了一个手机，回家不敢玩，上学放学的路上玩，这伤透了家长的脑筋。': 22,
                      '农村小学的家长为什么对自己孩子的学习不是那么关注，需要班主任反复地做工作？': 0,
                      '低年级是培养学生养成良好写字习惯的关键时期。虽然课堂上，重点进行了写字的指导，但是，一到实际写字时，有的学生并不是按你所讲的来写，对于这部分学生，如何培养良好的书写习惯？': 0,
                      '评价一个好老师的标准是什么？': 0,
                      '如何引导家长树立正确的教育观念？家庭是孩子的重要教育场所，家长不仅是孩子的第一任老师，也是孩子的终身老师。家长的教育理念很大程度上影响着孩子的整体发展。': 0,
                      '如何规范一年级学生的自我管理及行为习惯？': 0, '运用新教育理念评价一节好课的标准是什么?': 0, '请教新教育理念下评价一节好课的标准是什么？': 0,
                      '如何与包办型家长沟通？包办型家长的特点是孩子所有的事都包办代替，本应该孩子做的事，家长也全权代替了。孩子在学校，也一味地要求老师代劳。此类家长通常对孩子过于溺爱、过度呵护，长此以往，对孩子各方面能力的发展都十分不利。让他们树立正确的教养方式，能够更好地配合育人工作。': 0,
                      '如何搞好幼小衔接，让孩子尽快适应小学一年级的学习？': 0,
                      '很多老师会遇见这样一些学生，他们不喜欢听课，学习成绩不佳，经常被老师家长批评，却对挑战学校的规则、破坏课堂纪律、挑战老师的权威乐此不彼，从而博得非正向的关注，满足内心被关注的需求。如何正确引导这样的学生以维护校园秩序已成为不得不面对的现实问题。\n对于总是违反纪律的学生如何正确引导？帮助他们获取正向关注？在校园里，不乏一些淘气包，以挑战学校的规则、破坏课堂纪律、挑战老师的权威为能事，以取得非正向关注，满足内心被关注需要。': 5,
                      '日常教学中有哪些办法去关注学生？': 0,
                      '几年前的网络新闻里，曾有高中生质问“学三角函数有什么用，市场买菜找钱用得上吗？！”引发人们对现行教育与日常生活相脱离这一问题的关注。对于中小学生，他们见过杠杆，会做受力分析，可是他们不知道冲水马桶的水箱里面是怎样运作的、壁橱又是怎样固定的，他们学过自然，知道植物的根茎叶花，但他们不知道为何黄瓜叫“黄瓜”而不是“绿瓜”……\n怎么样可以做到陪孩子一起在生活里学习': 0,
                      '怎样开家长会才有实效呢？家长会是使学校教育与家庭教育保持密切联系、协调一致的有效形式和途径，也是学校整个教育教学工作的重要组成部分。': 0,
                      '如何看待违反学校纪律的学生？班级里总有些学生会违反课堂纪律，挑战校园规则。': 6,
                      '教师的“非常人”，就是我们要接纳每一个孩子，找到每个孩子的成长点。例如学生没有完成作业，我是认真了解原因？还是一味批评？我应当给他更多谅解还是鼓励？': 0,
                      '万平老师的小木桥在e时代利用博客、朋友圈创设了各种栏目：小桥播报、古事今听、新闻时钟、零点祝福、奥运心愿、学规讲堂等。每个孩子都可以经营自己的栏目，服务班级同学，孩子们通过自主管理也获得了成长。您如果做自己班上的小木桥，您想要设置哪些栏目呢？': 0,
                      '家长如何高效陪伴孩子写作业？': 0, '怎样指导一年级的孩子写好汉字？': 16,
                      '家长应该如何培养孩子的细心品质呢？在孩子作业的质量上，我们想让他高效地完成作业，但他有时候字迹特别潦草，口算什么的也会出现一些错误，马虎不认真。': 0,
                      '怎样鼓励和树立有特长却不愿、不敢参加活动的孩子的自信心？': 0,
                      '怎样帮助班级里自闭、不合群的学生？在班级里有这样一些孩子，学习成绩并不差，但却不喜欢和同学们一起玩，总是一个人静静地做自己的事情，沉浸在自己的世界里。他们很怕生，在陌生环境里非常沉默，好像特别早熟，对学校里发生的事不感兴趣，喜欢的东西也和普通小孩不一样，性格孤僻，面对教师的督促大多情况下会表现出抵触情绪。': 11,
                      '有什么写作亲子日记的经验吗？或推荐您认为比较适合的亲子互动游戏。': 0, '面对情绪失控的家长时，如何尽快安抚对方从而获得有效沟通？': 0,
                      '对于以下存在学生心理问题的学生该怎么办？\n（1）行为不足。这是指人们所期望的行为很少发生或从不发生。\n（2）行为过度。指某一类行为出现得太多。\n（3）行为不适当。指某些心理表现或行为在不适宜的情境中产生，但在适宜的条件下却又不发生。': 0,
                      '当您身处老师角色时，班上孩子出现哪些现象，需要进行性教育？': 0,
                      '南开创始人张伯苓曾说“强国必先强种，强种必先强身”以及“不懂体育的人不宜当校长”，点明体育育人对个人乃至对国家的重要作用。在学习蔡稳良《培养伴随孩子一生的运动习惯》视频之后，您觉得哪些方法可以用在提升本校体育育人水平上？又想到了哪些更适合本校的特色方法呢？': 0,
                      '怎样组织一堂有效的一年级数学课？': 0,
                      '教师在工作中会面临着来自不同方面的压力，学校布置的各项教学与非教学任务、学生形形色色的问题、与家长的沟通、和家人的相处……应接不暇的工作和耗费心力的人际交往常常令教师不知不觉中积累了很多负面情绪，对工作和生活造成影响，甚至会危害健康。教师如何觉察到自己需要心理调适，以便及时对教师的心理健康状况进行有效干预？': 0,
                      '欢如何开展家庭性教育，促进青少年的健康成长？。': 0, '平常孩子不怎么喜欢看书，怎样才能培养他的读书兴趣呢？': 17, '学生打架怎么办？老师应该怎么处理学生打架的问题？': 1,
                      '本次的课程中，您认为该校做好家校合作的主要原因是什么？从中收获到了哪些理念或方法？': 0, '日常有什么控制情绪的好方法呢？这种方法是否还有再优化的方式？': 0,
                      '如何才能培养教师的敬业精神，让他们在教书育人的工作中勤耕不辍呢？': 0,
                      '今天课程中的学校在提高家长会实效性的过程中让家长体会到了“被需要”的感觉，从而把家校合作的质量推上了一个新台阶。那么您认为，家长在哪些方面“被需要”呢？如何才能让家长感到自己“被需要”、以主动付出和投入呢？': 0,
                      '如何让孩子获得幸福感和取得成功？': 0,
                      '写作业已占据学生生活的大部分时间，督促或陪伴孩子写完作业成为家长们每天晚上的“艰巨任务”。很多孩子写作业时磨磨蹭蹭、难以专注，每晚“例行”的吼叫或是全程监督效果不佳，反而让家长身心俱疲，还让亲子关系更加紧张。什么简单有效的好办法能让孩子高效、自主地完成作业？有智慧的家长在陪伴孩子写作业的过程中会做什么、不会做什么呢？': 0,
                      '“雄起爸爸团”的故事令人印象深刻。在您的班上，有哪些类似的主题班会或沙龙呢？': 0, '您认为在帮助问题学生时最关键的是什么？': 0,
                      '由于社会及家庭对特需的认知存在一定偏差，教师在学校培养孩子的良好习惯，家长对于孩子习惯的养成却不够重视，导致班里孩子的差距较大。有些家长不认为孩子特殊，教师得不到家长的积极配合，反复劝导，但收效甚微。教师缺乏专业指导，找不到好的办法去疏导心理行为偏差（攻击倾向、多动倾向、自闭倾向、缺乏自控力等）的学生。面对这种情况，老师们该如何与家长沟通，建立满足特殊学生需求的家校协作教育机制？': 0,
                      '如何做到家委会的活动体系化？欢迎分享促进家委会常态化、体系化的方法。': 0,
                      '还记得那个制作蜘蛛侠盔甲的体育老师吗？你觉得自己有什么优点呢？在日常工作中有哪些擅长的地方？这些优点在学校工作中能够如何得到更好的发挥呢？': 0,
                      '学习课程后，请老们尝试结合本班情况，总结帮助问题学生时可以采用哪有效策略？': 0,
                      '一位小学三年级的班主任提出这样的困惑，有这样一类学生，上课时常常走神，老师多次提醒也很难让他专心听讲。课后的作业迟迟交不上来，与家长沟通后家长表示在家一直要求孩子写作业，但孩子没写一会儿又去做其他事，自控力依旧很差。作为班主任该如何引导他们不断提高自控力？': 18,
                      '在本周的课程中，清华附小介绍了家委会管理和运行的系统架构，您还记得这个体系里有哪些部分吗？请试着把这个框架复述出来，并就其中的部分内容谈谈您的看法。': 0,
                      '作为一名校长，您学校是如何评价教师的？在这一评价基础上，如何能够丰富维度，体现教师的发展呢？': 0,
                      '学生们要面对学业上的压力，家长在教育孩子方面也遇到越来越多的烦恼。如果说孩子的成长需要父母自身的成长做驱动，那么在这个过程中，家长该秉持怎样的育人理念，才能培养孩子养成良好的学习、生活习惯？': 0,
                      '您认为家校合作的“江西模式”有哪些经验可以借鉴呢？': 0,
                      '作为老师，我们期望从哪方面提升和改善自己，让我的教师生涯更有价值呢？作为校长，如何评价和激励本校老师才会更加提升教师的积极性和职业幸福感呢？': 0,
                      '家长为什么会站在老师的对立面？这样做对他孩子的教育有好处吗？问题家长一定会造化出一个问题孩子。': 0,
                      '班里有几个成绩极差的学生，而且课堂表现也不好，每次上课提问，几乎都回答不出来。想咨询一下各位老师，对待这样的学生，如果上课提问他们，会特别耗费时间，但是不提问，他们就肯定一点都不听。那这种孩子，究竟在课上应如何对待呢？': 16,
                      '崇文实验学校是如何引导家长认同学校的教育理念的？您所在的学校在这方面如何探索呢？': 0,
                      '在团队中学会赏识他人，先从自己身边的同事开始。请回想日常工作中，和你合作最多的同事，多多列举他的优点吧。': 0, '期末如何帮助孩子有效的复习。': 0, '家校沟通的策略有哪些？': 0,
                      '有些农村留守儿童，父母外出打工，把学生交给老人照顾，没有教育，只解决了温饱，更谈不上学生的思想教育。对于这样的学生怎样开展更好的家校合作呢？': 0,
                      '怎样让孩子树立自信，变得活泼开朗？': 0, '如何做一个幸福的好老师？': 0, '如何提高学生的自控能力？': 0, '为什么周末、节假日学生作业比较差？': 0,
                      '学珠心算有什么好处吗？珠心算应该被推崇吗？': 0, '老师经常会对学生对自己的家人发火生气，那么我们应该如何处理好老师自己的情绪呢？': 0,
                      '长期从事各种职业的人都可能面临的职业倦怠的问题，体现为情感、态度和行为的衰竭，对工作极为不利，更会严重损害人们的身心健康，应当尽早预防、妥善应对，对于教师而言，有什么好的方法来避免陷入职业倦怠呢？': 0,
                      '培养学生自主管理和自我教育能力的关键是什么？': 0, '如何培养学生学习的兴趣，积极主动学习': 17, '怎样才能做到赏识教育': 0,
                      '面对经过多次口头教育，讲道理，叫家长，仍然不知道改错，三天两头犯错的学生，教师到底该怎么办？': 20,
                      '如何开发与实施家校共育课程，更好地发挥学校与家庭的育人作用，共同促进学生个体的发展？': 0, '怎样帮助初三学生更快更准的记住方程式？': 0,
                      '如何培养小学生养成喜欢看书的好习惯？': 0, '怎样强化学生的心理素质': 0, '怎样培养学生自主学习的习惯?': 0, '老师应该怎样培养学生认真倾听的习惯？': 0,
                      '学生在课堂上总控制不住与周围同学讲小话，有何妙招可解决?': 5, '志于道、据于德、依于仁、游于艺，那么如何培养出德艺双馨的孩子？': 0, '如何激发班主任工作活力？': 0,
                      '陶行知先生说过：“最好的教育是教育学生自己做好自己的先生。”就是要让学生养成长期自我教育，自我管理的好习惯，并持之以恒。一二年级是学生学习习惯养成的关键时期，但是，对于部分低年级学生来说，在自主学习习惯培养中却还存在不少问题，那么，教师怎样引导才能从内心深处激发他们学习的动力？让他们在科学的教育过程中各方面行为潜移默化地得到强化，学会自主学习，从而慢慢地养成良好的学习习惯，感受学习带给他们的快乐。': 0,
                      '如何让小学孩子上好英语课？有英语课就完成任务，没有就几乎不翻书。': 0,
                      '孩子从幼儿园升入一年级，要面对学习、生活、人际环境的重大改变。其中要面临的最大的问题是学校对学生的行为习惯提出了很多约束性的要求，各项行为规范严格，学生要能够快速地从自由散漫的幼儿转变为守纪律、懂礼貌、爱学习的小学生。这些规范对刚入学的孩子来说要求较高，容易让他们产生负面情绪，对老师、同学、学校产生抵触心理。作为教师，您会怎样培养一年级学生的良好行为习惯，帮助他们更好地适应小学生活？': 0,
                      '如何培养低年级孩子学会认真倾听与思考?': 0, '时间是一种重要的资源': 0,
                      '最近一位家长向班主任老师诉苦：自己的儿子活泼好动，每天回到家里不先写作业，而是先吃东西、玩玩具、看电视，磨蹭到很晚才想起有作业要做。他的爸爸时常批评他，但他却没有丝毫改进。早上去上学时无精打采，还总觉得学习没意思，上学只是为了和同学们一起玩耍。他的这种学习状态，让家长很担心。作为老师，应该如何激发孩子学习的自觉性？': 17}


def modelwithTopicInfo(result_name):
    predic_res = []
    # result_name = './../02BERT_LSTM_Pooling_MLP/02bert_lstm_mlp_predict.csv'
    with open(result_name, 'r', encoding='utf-8') as fcsv:
        csv_reader = csv.reader(fcsv)  # 使用csv.reader读取csvfile中的文件
        for row in csv_reader:
            predic_res.append(int(row[0]))
    print('得到模型对100对问题语句的预测结果')
    print(predic_res)

    #这里只考虑后50个不是相似语句， 但是被错误分成相似语句的情况，这种情况可以通过topic信息来纠正
    wrong_label_for_no_same_sentences_index = []
    wrong_label_for_same_sentences_index = []
    for index in range(len(predic_res)):
        if index<50:
            if predic_res[index] == 0:
                wrong_label_for_same_sentences_index.append(index)
        # print('分错语句对的索引', wrong_label_for_no_same_sentences_index)

        if index >=50:
            if predic_res[index] == 1:
                wrong_label_for_no_same_sentences_index.append(index)
    print('相似语句对却分错的个数', len(wrong_label_for_same_sentences_index))
    print('分错语句对的索引', wrong_label_for_no_same_sentences_index)
    print('分错语句对的个数', len(wrong_label_for_no_same_sentences_index))

    #读取全部测试语句，选取分错的句子
    sen_file_name = './test_sentences_pairs_100.csv'
    all_sens = []
    with open(sen_file_name, 'r', encoding='utf-8') as fcsv:
        csv_reader = csv.reader(fcsv)  # 使用csv.reader读取csvfile中的文件
        for row in csv_reader:
            all_sens.append(row)

    wrong_sentens = []
    for index in wrong_label_for_no_same_sentences_index:
        wrong_sentens.append(all_sens[index])
    #通过topic统计可以纠正的个数
    count = 0
    for wrong_s in wrong_sentens:

        s1 = wrong_s[0]
        s2 = wrong_s[1]
        t_id1 = sentences_ann_dict[s1]
        t_id2 = sentences_ann_dict[s2]
        # print(t_id1, t_id2)
        if t_id1 != t_id2:
            if t_id1==0 and t_id2 == 0:
                continue
            else:
                count +=1
    print(count)



if __name__ == '__main__':
    print('获取语句标注情况的字典')
    if not os.path.exists('sentences_ann_dict.json'):
        sentences_ann_dict = {}
        question_ann_file_path = r'question_ann.xls'
        data = xlrd.open_workbook(question_ann_file_path)
        table = data.sheet_by_name('Sheet1')
        nrows = table.nrows
        ncols = table.ncols
        for index_row in range(1,nrows):
            senten = table.cell(index_row, 1).value
            topic_info = table.cell(index_row, 0).value
            # print(type(topic_info) == str)
            if type(topic_info) == str:
                topic_id = 0
            else:
                topic_id = int(topic_info)
            if senten not in sentences_ann_dict:
                sentences_ann_dict[senten] = topic_id
        with open('sentences_ann_dict.json', 'w', encoding='utf-8') as f:
            json.dump(sentences_ann_dict, f, ensure_ascii=False)


    print('count model result with topic info')
    result_name2 = './../02BERT_LSTM_Pooling_MLP/02bert_lstm_mlp_predict.csv'
    modelwithTopicInfo(result_name2)

    result_name3 = './../03BERT_MLP/03bert_mlp_predict.csv'
    modelwithTopicInfo(result_name3)

    result_name4 = './../04BERT_LSTM_Pooling_MLP_with_LQCMC/04bert_lstm_mlp_predict.csv'
    modelwithTopicInfo(result_name4)

    result_name5 = './../05BERT_MLP/05bert_mlp_predict.csv'
    modelwithTopicInfo(result_name5)