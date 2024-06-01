import Logger from "../config/logger";

class ClothingBinStorage {
    private static instance: ClothingBinStorage;

    constructor(){
        // TODO
        //connect db
    };

    public static getInstance(): ClothingBinStorage {
        if (!this.instance) {
            this.instance = new ClothingBinStorage();
            Logger.getInstance().info("ClothingBinStorage instance created");
        }
        return this.instance;
    };

    public static async getClothingBins(lat: number, lon: number): Promise<any> {
        Logger.getInstance().info(`ClothingBinStorage getClothingBins called`);
        Logger.getInstance().info(`lat: ${lat}, lon: ${lon}`);
        const dummyData = {
            info:[
            {
                id: 1,
                dong: "팔달구",
                address: "경기도 수원시 권선구 권선 1동 수원시청역",
                lat: 37.261851,
                lon: 127.031121
            },
            {
                id: 2,
                dong: "팔달구",
                address: "경기도 수원시 팔달구 효원로 307번길 20",
                lat: 37.261890232996635,
                lon: 127.03742802143097
            }
        ]};
        return new Promise((resolve, reject) => {
            resolve(dummyData);
        });
    };
}

export default ClothingBinStorage;