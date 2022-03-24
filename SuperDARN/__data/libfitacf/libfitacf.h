#ifndef __LIBFITACF_H__
#define __LIBFITACF_H__
#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <map>
#include "listmapkeys.h"
#include "fitacf.h"
#endif



int GetNewRandomNumber();


bool CheckMapKey(int I);


extern "C" {
	int Loadfitacf(const char *fname, bool Verbose);
	int GetScalarLen(int I);
	void GetScalars(int I, int *Date, float *ut, int *Beam, int *Channel,
						int *ScanCode, int *nGates, int *smsep, 
						int *lagfr, int *ArrLen, int *RecLen, int *na, 
						long int *ArrOffset);
	void Delfitacf(int I);		
}
/* map which will contain the instances of fitacf */
extern std::map<int,fitacf*> acfmap;
