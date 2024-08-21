import { Request, Response } from "express";
import Logger from "../../config/logger";
import ClothBox from "../../models/ClothBox";

class HomeController {

    public async processSearch(req: Request, res: Response): Promise<void> {
        Logger.getInstance().info(
            `POST /search 200 Request: ${JSON.stringify(req.body)}`
        );
        const clothBox = new ClothBox(req.body);   
        const response = await clothBox.search();
        if (response.err)
            Logger.getInstance().error(
                `POST /search 200 Response: Fail, ${response.err}`
            );
        else
            Logger.getInstance().info(
                `POST /search 200 Response: Success`
            );
        res.status(200).json(response);
    }
}

export default HomeController;