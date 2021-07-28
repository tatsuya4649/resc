export const ERR={flag:1<<0,explain:"Normal error"};
export const EME={flag:1<<1,explain:"Emergency header"};
export const DEF={flag:1<<2,explain:"Defination error"};
export const ROG={flag:1<<3,explain:"RescLog error"};
export const SSH={flag:1<<4,explain:"SSH error"};
export const REM={flag:1<<5,explain:"Remote host error"};
export const LOC={flag:1<<6,explain:"Local host error"};
export const MNF={flag:1<<7,explain:"Module not found error"};
export const IMP={flag:1<<8,explain:"Import error"};
export const FUN={flag:1<<9,explain:"Trigger function error"};
export const IND={flag:1<<10,explain:"Indent error"};
export const NFS={flag:1<<11,explain:"Not found script error"};

const SFlagList = Array();
SFlagList.push(ERR);
SFlagList.push(EME);
SFlagList.push(DEF);
SFlagList.push(ROG);
SFlagList.push(SSH);
SFlagList.push(REM);
SFlagList.push(LOC);
SFlagList.push(MNF);
SFlagList.push(IMP);
SFlagList.push(FUN);
SFlagList.push(IND);
SFlagList.push(NFS);

export function getflag_exlist(sflag){
	var explains = []
	for (const value of SFlagList){
		if (typeof(value) != 'object'){
			continue;
		}
		if ((value.flag&sflag) != 0){
			explains.push(value.explain);
		}
	}
	return explains;
}
