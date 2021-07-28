import * as UploadFileType from "../types/UploadFile";
import axios from "axios";

export function analyzeFile(file){
	return function(dispatch){
		dispatch({'type':UploadFileType.ANALYZING});
		const formdata = new FormData();
		formdata.append("logfile",file)
		//axios.post(`${location.origin}`,formdata)
		axios.post('http://localhost:11111',formdata)
		.then(response => {
			const data = response.data;
			const result = data.result;
			if (result == "success"){
				dispatch({'type':UploadFileType.ANALYZED,'payload': data.analyze});
			}else{
				throw new Error("result is failure.");
			}
		})
		.catch(err => {
			console.log(err);
			dispatch({'type':UploadFileType.ERROR});
		});
	}
}

export function analyzedFile(filename){
	return {
	'type':UploadFileType.ANALYZED,
	'logfile':filename
	}
}
