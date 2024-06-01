import { Request, Response } from "express";
import Logger from "../../config/logger";

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
    }
}

export default HomeController;