// ClosestFill.cpp
// - Replaces 0-colored pixels with a closest non-0 color in an 8 bit BMP
// - Expects 2 bmp file names (in and out) as parameters

#include "stdafx.h"
#include "BMPFace.hpp"

#include <string>

struct ClosestPoint
{
	int x;
	int y;
	float dist;
};

int main(int arg_c, char* arg_v[])
{
	if (arg_c < 3)
		return 0;

	std::string s_in = arg_v[1];
	std::string s_out = arg_v[2];

	Bitmap<unsigned char> bmp;
	bmp.Load(s_in);
	Bitmap<unsigned char> out = bmp;

	std::vector<ClosestPoint> cp;
	cp.resize(bmp.GetHeight()*bmp.GetWidth());

	for (auto &p : out)
	{
		int index = p.y*bmp.GetWidth() + p.x;
		if (p.value != 0)
		{
			cp[index] = ClosestPoint{p.x,p.y,0.f};
		}
		else
		{
			cp[index] = ClosestPoint{ -1,-1,999999.f };
		}
	}

	int iter = max(bmp.GetHeight(), bmp.GetWidth())*2;

	bool over = false;
	while (!over)
	{
		over = true;
		for (auto &p : out)
		{
			int index = p.y*out.GetWidth() + p.x;
			if (cp[index].dist <= 0.f) continue;
			auto apt = out.Aperture(p.x, p.y);
			for (auto& point : apt)
			{
				int pindex = point.y*out.GetWidth() + point.x;
				if ((cp[pindex].x == cp[index].x) && (cp[pindex].y == cp[index].y))
					continue;
				if (cp[pindex].dist >= cp[index].dist) continue;
				float dx = (p.x - cp[pindex].x);
				float dy = (p.y - cp[pindex].y);
				float ndist = dx*dx + dy*dy;
				if (ndist < cp[index].dist)
				{
					over = false;
					cp[index].dist = ndist;
					cp[index].x = cp[pindex].x;
					cp[index].y = cp[pindex].y;
				}
			}
		}

		if (iter-- <= 0) break;
	}

	for (auto &p : out)
	{
		int index = p.y*out.GetWidth() + p.x;
		if (bmp.Check(cp[index].x, cp[index].y))
			p.value = bmp.At(cp[index].x, cp[index].y);
	}

	out.Save(s_out);

    return 0;
}

