import express, { Router } from 'express';
import HomeController from './home.ctrl'

class HomeRouter {
    private router: Router;
    private homeController: HomeController;

    constructor(){
        this.router = express.Router();
        this.homeController = new HomeController();
        
        this.initRoutes();
    }

    private initRoutes(){
        this.router.get("/", this.homeController.outputHome);
        this.router.post("/search", this.homeController.processSearch);
    }

    public getRouter(): Router{
        return this.router;
    }
}

export default HomeRouter;