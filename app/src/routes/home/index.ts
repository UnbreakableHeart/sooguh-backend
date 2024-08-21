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
        this.router.post("/search", this.homeController.processSearch
            /*
            #swagger.tags = {
                name: 'default',
            }
            #swagger.summary = 'Search for clothboxes'
            #swagger.description = 'Search for clothboxes'
            #swagger.requestBody = {
                required: true,
                content: {
                    "application/json": {
                        schema: {
                            $ref: "#/components/schemas/CurrentLocation"
                        }  
                    }
                }
            } 
            #swagger.responses[200] = { 
                schema: { $ref: "#/components/schemas/ClothBox" },
                description: 'Successful search'
            }
            #swagger.responses[400] = { 
                description: 'Error in search'
            }
            */
        );
    }

    public getRouter(): Router{
        return this.router;
    }
}

export default HomeRouter;