import React from "react";
import { BrowserRouter,Route,Switch} from "react-router-dom";
import AnalyzeDetail from "../pages/AnalyzeDetail";
import AnalyzeList from "../pages/AnalyzeList";

export default class Main extends React.Component{
	render(){
		return (
		<main>
		<BrowserRouter>
		<Switch>
			<Route exact path="/" component={AnalyzeList} />
			<Route exact path="/detail" component={AnalyzeDetail} />
		</Switch>
		</BrowserRouter>
		</main>
		);
	}
}
