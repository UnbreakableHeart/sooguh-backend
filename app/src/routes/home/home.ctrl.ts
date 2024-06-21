import { Request, Response } from "express";
import Logger from "../../config/logger";
import ClothBox from "../../models/ClothBox";

class HomeController {
    
    constructor(){
    }

    public outputHome(req: Request, res: Response): void {
        Logger.getInstance().info(`GET / 200 "홈 화면 출력"`);
        res.status(200).json({
            message: "홈 화면 출력"
        });
        // TODO: render
        // res.render("home/index");
    };

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