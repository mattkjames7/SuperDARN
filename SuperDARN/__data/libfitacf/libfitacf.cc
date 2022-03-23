#include "libfitacf.h"

/* map which will contain the instances of fitacf */
std::map<int,fitacf*> acfmap;


/* flag to say whether the random number generator has been intialized */
bool seeded = false;

int GetNewRandomNumber() {
	/* init random seed */
	if  (seeded == false) {
		srand(time(NULL));
		seeded = true;
	}
	
	/* get the random number identifier */
	bool done = false;
	int I;
	while (done == false) {
		I = rand();
		if (hasMapKey(I,lt1Dinst) == false) {
			done = true;
		}
	}
	
	return I;
}	

bool CheckMapKey(int I) {
	
	/* check that the map contains this instance */
	if (hasMapKey(I,acfmap)) {
		return true;
	} else {
		printf("Invalid fitacf object instance provided!");
		return false;
	}

}



int Loadfitacf(const char *fname, bool Verbose) {
	
	/* get the random number */
	int I = GetNewRandomNumber();
	
	/* create the object */
	acfmap[I] = new fitacf(fname,Verbose);

	return I;
}

int GetScalarLen(int I) {
	if (CheckMapKey(I)) {
		return acfmap[I]->GetScalarLen();
	} else {
		return -1;
	}
}

void GetScalars(int I, int *Date, float *ut, int *Beam, int *Channel,
						int *ScanCode, int *nGates, int *smsep, 
						int *lagfr, int *ArrLen, int *RecLen, int *na, 
						long int *ArrOffset) {

	if (CheckMapKey(I)) {
		acfmap[I]->GetScalars(Date,ut,Beam,Channel,ScanCode,nGates,
								smsep,lagfr,ArrLen,RecLen,na,ArrOffset);
	}

}

int GetArrayLen(int I) {
	if (CheckMapKey(I)) {
		return acfmap[I]->GetArrayLen();
	} else {
		return -1;
	}
}

void GetArrays(int I, Date, float *ut, int *Beam, int *Channel,
						int *ScanCode, int *nGates, int *smsep, 
						int *lagfr, float *V, float *P_l, float *W_l,
						int *Gnd, int *Gate) {

	if (CheckMapKey(I)) {
		acfmap[I]->GetArrays(Date,ut,Beam,Channel,ScanCode,nGates,smsep, 
								lagfr,V,P_l,W_l,Gnd,Gate);
	}

}

void Delfitacf(int I) {
	std::map<int,fitacf*>::iterator it;
	
	if (CheckMapKey(I)) {
		it = acfmap.find(I);
		acfmap.erase(it);
	}
}
