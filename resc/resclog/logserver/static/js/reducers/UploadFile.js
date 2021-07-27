import * as UploadFileType from "../types/UploadFile";

export default function reducer(state={
	logfiles: [],
	analyzing: false,
	analyzed: false,
	error: null
},action){
	switch (action.type){
	case UploadFileType.ANALYZING:
		return {...state,analyzing: true}
	case UploadFileType.ANALYZED:
		return {...state,logfiles: [...state.logfiles,action.logfile],analyzing: false,analyzed: true}
	}
	return state;
}

