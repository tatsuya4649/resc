import * as UploadFileType from "../types/UploadFile";

export function analyzeFile(file){
	return function(dispatch){
		dispatch({'type':UploadFileType.ANALYZING});
	}
}

export function analyzedFile(filename){
	return {
	'type':UploadFileType.ANALYZED,
	'logfile':filename
	}
}
