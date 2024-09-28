import ClothBox from "../app/src/models/ClothBox";
import ClothBoxStorage from "../app/src/models/ClothBoxStorage";

jest.mock("../app/src/models/ClothBoxStorage");

describe("ClothBox", () => {
    let clothBox: ClothBox;
    let mockClothBoxStorage: any;
    let mockBody: any;

    beforeEach(() => {
        mockClothBoxStorage = {
            getClothBoxes: jest.fn(),
        };
        (ClothBoxStorage.getInstance as jest.Mock).mockReturnValue(mockClothBoxStorage);
        mockBody = {
            coordinates: {
                lat: 37.162720658936784,
                lon: 127.11264145768898,
            },
            distance: 3000,
        };
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    it("search for cloth boxes and return a formatted response", async () => {
        const mockClothBoxes = [
            { _id: "1", address: "Address 1", location: { coordinates: [127.11264145768898, 37.162720658936784] } },
            { _id: "2", address: "Address 2", location: { coordinates: [127.11264145768898, 37.162720658936784] } },
        ];

        mockClothBoxStorage.getClothBoxes.mockResolvedValue(mockClothBoxes);

        clothBox = new ClothBox(mockBody);

        const result = await clothBox.search();
        expect(result.length).toBe(2);
        expect(result[0]).toHaveProperty("_id");
        expect(result[0]).toHaveProperty("address");
        expect(result[0]).toHaveProperty("coordinates");
        expect(result[0].coordinates).toHaveProperty("lon");
        expect(result[0].coordinates).toHaveProperty("lat");
    });

    it("handle errors when searching for cloth boxes", async () => {
        const mockError = new Error("Test Error");
        mockClothBoxStorage.getClothBoxes.mockRejectedValue(mockError);
        clothBox = new ClothBox(mockBody);

        const result = await clothBox.search();

        expect(result).toEqual(mockError);
    });

    it("return empty array when no cloth boxes are found", async () => {
        mockClothBoxStorage.getClothBoxes.mockResolvedValue([]);
        clothBox = new ClothBox(mockBody);

        const result = await clothBox.search();

        expect(result).toEqual([]);
    });

    it("return cloth boxes within the specified distance", async () => {
        const mockClothBoxes = [
            { _id: "1", address: "Address 1", location: { coordinates: [127.11264145768898, 37.162720658936784] } },
            { _id: "2", address: "Address 2", location: { coordinates: [127.11264145768898, 37.162720658936784] } },
        ];
        mockClothBoxStorage.getClothBoxes.mockResolvedValue(mockClothBoxes);
        clothBox = new ClothBox(mockBody);

        const result = await clothBox.search();

        expect(result).toEqual([
            { _id: "1", address: "Address 1", coordinates: { lat: 37.162720658936784, lon: 127.11264145768898 } },
            { _id: "2", address: "Address 2", coordinates: { lat: 37.162720658936784, lon: 127.11264145768898 } },
        ]);
    });
});