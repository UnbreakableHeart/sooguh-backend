import ClothBoxStorage from "../app/src/models/ClothBoxStorage";

describe("ClothBoxStorage", () => {
    let clothBoxStorage: ClothBoxStorage;

    beforeAll(async () => {
        clothBoxStorage = ClothBoxStorage.getInstance();
    });

    it("get cloth boxes around 1000 meters", async () => {
        const lat = 37.162720658936784; 
        const lon = 127.11264145768898; 
        const distance = 1000; 

        const result = await clothBoxStorage.getClothBoxes(lat, lon, distance);

        expect(result).toBeInstanceOf(Array);
        expect(result.length).toBe(0);
    });

    it("get cloth boxes around 3000 meters", async () => {
        const lat = 37.162720658936784;
        const lon = 127.11264145768898; 
        const distance = 3000; 

        const result = await clothBoxStorage.getClothBoxes(lat, lon, distance);

        expect(result).toBeInstanceOf(Array);
        expect(result.length).toBe(10);
    });

    it("get cloth boxes around 5000 meters", async () => {
        const lat = 37.162720658936784;
        const lon = 127.11264145768898; 
        const distance = 5000; 

        const result = await clothBoxStorage.getClothBoxes(lat, lon, distance);

        expect(result).toBeInstanceOf(Array);
        expect(result.length).toBe(541);
    });
});