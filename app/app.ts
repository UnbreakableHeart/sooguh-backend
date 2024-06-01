import express from "express";
import Logger from "./src/config/logger";
// import dotenv from "dotenv";

const logger = Logger.getInstance();

class App{
    private application: express.Application;

    constructor(){
        this.application = express();
        this.initMiddleware();
        this.initRoutes();
    };
    private initMiddleware(){
        // this.application.use(express.json());
        // this.application.use(express.urlencoded({extended: false}));
    };

    private initRoutes(){
        this.application.get("/", (req, res) => {
            res.status(200).json({
                message: "Hello World"
            });
        });
    };

    public getApplication(): express.Application{
        return this.application;
    };
}

const app = new App().getApplication();

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => logger.info(`Listen on port ${PORT}`));