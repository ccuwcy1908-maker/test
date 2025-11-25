import { ItineraryData, BackupPlan } from './types';

export const MEMBERS = ["ChiYeh", "Olivia", "Yue", "May"];

export const ITINERARY: ItineraryData = {
  "Day 1": {
    date: "2025-12-05",
    items: [
      {
        time: "15:00",
        title: "✈️ 抵達/Check-in",
        desc: "機場快線 AREX 直達弘大，先去飯店放行李。",
        transport: "AREX 機場快線",
        lat: 37.5575,
        lon: 126.9245,
        loc: "弘大入口站"
      },
      {
        time: "18:00",
        title: "🍽 小豬存錢筒",
        desc: "弘大必吃石頭烤肉，石頭上烤的豬五花。",
        transport: "步行前往",
        lat: 37.5559,
        lon: 126.9230,
        loc: "Piggy Bank Stone Grill"
      },
      {
        time: "20:00",
        title: "🛍 弘大商圈",
        desc: "街頭表演、美妝、買衣服、拍貼機。",
        transport: "步行",
        lat: 37.5563,
        lon: 126.9225,
        loc: "弘大商圈"
      }
    ]
  },
  "Day 2": {
    date: "2025-12-06",
    items: [
      {
        time: "11:00",
        title: "🥩 馬場洞韓牛",
        desc: "頂級 1++ 韓牛，入口即化 (推薦龍門家)。",
        transport: "5號線 馬場站 2號出口",
        lat: 37.5670,
        lon: 127.0420,
        loc: "馬場洞畜產物市場"
      },
      {
        time: "14:00",
        title: "📷 證件照拍攝",
        desc: "韓式精修證件照，記得帶妝。",
        transport: "地鐵移動",
        lat: 37.5560,
        lon: 126.9240,
        loc: "Photostudio"
      },
      {
        time: "15:30",
        title: "🛍 龍山 I’Park",
        desc: "超大購物中心，有龍貓展、相機街。",
        transport: "1號線 龍山站",
        lat: 37.5298,
        lon: 126.9647,
        loc: "I'Park Mall"
      },
      {
        time: "18:30",
        title: "🍲 一隻雞 (晚餐)",
        desc: "陳玉華或孔陵，蒜味濃郁雞湯。",
        transport: "4號線 東大門站",
        lat: 37.5709,
        lon: 127.0062,
        loc: "陳玉華一隻雞"
      },
      {
        time: "20:30",
        title: "🍸 梨泰院酒吧",
        desc: "Fountain / Thursday Party，異國風情夜生活。",
        transport: "6號線 梨泰院站",
        lat: 37.5340,
        lon: 126.9940,
        loc: "梨泰院"
      }
    ]
  },
  "Day 3": {
    date: "2025-12-07",
    items: [
      {
        time: "10:30",
        title: "🐷 金豬食堂",
        desc: "米其林推薦，最好吃的烤豬頸肉 (需排隊)。",
        transport: "3號線 藥水站",
        lat: 37.5590,
        lon: 127.0100,
        loc: "金豬食堂"
      },
      {
        time: "13:30",
        title: "🛍 明洞商圈",
        desc: "Olive Young 旗艦店、明洞聖堂。",
        transport: "4號線 明洞站",
        lat: 37.5630,
        lon: 126.9840,
        loc: "明洞商圈"
      },
      {
        time: "18:00",
        title: "🍽 無垢屋",
        desc: "清淡牛肉湯 (Gomguk)，舒緩腸胃。",
        transport: "1號線 市廳站",
        lat: 37.5650,
        lon: 126.9790,
        loc: "無垢屋"
      }
    ]
  }
};

export const BACKUP_PLANS: BackupPlan[] = [
  { name: "Coex 星空圖書館", desc: "室內雨天備案，絕美書牆。" },
  { name: "漢南洞", desc: "設計師品牌聚集地。" },
  { name: "樂天超市 (首爾站)", desc: "伴手禮採買。" }
];