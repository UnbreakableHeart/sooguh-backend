import express from "express";
import Logger from "./src/config/logger";
import dotenv from "dotenv";
import HomeRouter from "./src/routes/home";
import DatabaseSingleton from "./src/config/db";

const logger = Logger.getInstance();
class App{
    private application: express.Application;

    constructor(){
        this.application = express();
        this.initConfig();
        this.initMiddleware();
        this.initRoutes();
    };

    private initConfig(){
        dotenv.config();
        DatabaseSingleton.getInstance().connect();
    };

    private initMiddleware(){
        this.application.use(express.json());
        this.application.use(express.urlencoded({extended: true}));
    };

    private initRoutes(){
        const home = new HomeRouter().getRouter();
        this.application.use("/", home);
    };

    public getApplication(): express.Application{
        return this.application;
    };
}

const app = new App().getApplication();

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => logger.info(`Listen on port ${PORT}`));