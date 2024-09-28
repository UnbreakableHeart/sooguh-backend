import { Request, Response } from "express";
import HomeController from "../app/src/routes/home/home.ctrl";
import ClothBox from "../app/src/models/ClothBox";

jest.mock("../app/src/models/ClothBox");

describe("HomeController", () => {
    let req: Partial<Request>;
    let res: Partial<Response>;
    let jsonMock: jest.Mock;
    let statusMock: jest.Mock;

    beforeEach(() => {
        req = {
            body: { key: "value" }
        };
        jsonMock = jest.fn();
        statusMock = jest.fn(() => ({ json: jsonMock }));
        res = {
            status: statusMock
        };
        jest.clearAllMocks();
    });

    it("should log request and response success", async () => {
        const mockClothBoxes = [
            {
                _id: "1",
                address: "Test Address 1",
                coordinates: {
                    lon: 123,
                    lat: 456,
                },
            },
        ];
        const mockSearch = jest.fn().mockResolvedValue(mockClothBoxes);
        (ClothBox as jest.Mock).mockImplementation(() => ({
            search: mockSearch
        }));

        const homeController = new HomeController();
        await homeController.processSearch(req as Request, res as Response);

        expect(mockSearch).toHaveBeenCalled();
        expect(statusMock).toHaveBeenCalledWith(200);
        expect(jsonMock).toHaveBeenCalledWith(mockClothBoxes);
    });

    it("should log request and response failure", async () => {
        const mockSearch = jest.fn().mockResolvedValue({ err: "Test Error" });
        (ClothBox as jest.Mock).mockImplementation(() => ({
            search: mockSearch
        }));

        const homeController = new HomeController();
        await homeController.processSearch(req as Request, res as Response);

        expect(mockSearch).toHaveBeenCalled();
        expect(statusMock).toHaveBeenCalledWith(200);
        expect(jsonMock).toHaveBeenCalledWith({ err: "Test Error" });
    });
});