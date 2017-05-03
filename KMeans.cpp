// Ronak Kumar (2015080)

#include <bits/stdc++.h>
using namespace std;
class Point
{
	int clusterID, pointID;
	vector<double> values;
	int total;
	string name;
	public:
		Point(int pointID, vector<double>& values, string name = "")
		{
			this->pointID = pointID;
			total = values.size();
			for(int i = 0; i < total; i++)
				this->values.push_back(values[i]);
			this->name = name;
			clusterID = -1;
		}
		int getID();
		void setCluster(int);
		int getCluster();
		double getValue(int);
		int getTotal();
		void addValue(double);
		string getName()
		{
			return this->name;
		}
};
int Point::getID()
{
	return this->pointID;
}
void Point::setCluster(int clusterID)
{
	this->clusterID = clusterID;
}
int Point::getCluster()
{
	return this->clusterID;
}
double Point::getValue(int index)
{
	return values[index];
}
int Point::getTotal()
{
	return this->total;
}
void Point::addValue(double value)
{
	values.push_back(value);
}
class Cluster
{
	int clusterID;
	vector<double> value;
	vector<Point> points;
	public:
		Cluster(int clID, Point pt)
		{
			this->clusterID = clID;
			int total_values = pt.getTotal();
			for(int i = 0; i < total_values; i++)
				value.push_back(pt.getValue(i));
			points.push_back(pt);
		}
		void addPoint(Point);
		bool removePoint(int);
		double getValue(int);
		void setValue(int, double);
		Point getPoint(int idx);
		int getTotal();
		int getID();
};
void Cluster::addPoint(Point pt)
{
	points.push_back(pt);
}
bool Cluster::removePoint(int pointID)
{
	int total = points.size();
	for(int i = 0; i < total; i++)
	{
		if(points[i].getID() == pointID)
		{
			points.erase(points.begin() + i);
			return true;
		}
	}
	return false;
}
double Cluster::getValue(int idx)
{
	return value[idx];
}
void Cluster::setValue(int idx, double newValue)
{
	value[idx] = newValue;
}
Point Cluster::getPoint(int idx)
{
	return points[idx];
}
int Cluster::getTotal()
{
	return points.size();
}
int Cluster::getID()
{
	return clusterID;
};
class KMeans
{
	int k, values, points, iterations;
	vector<Cluster> clusters;
	int getNearestCenter(Point pt)
	{
		double sum = 0.0;
		double minDistance;
		int clusterCenter = 0;
		for(int i = 0; i < values; i++)
			sum += pow(clusters[0].getValue(i) - pt.getValue(i), 2.0);
		minDistance = sqrt(sum);
		for(int i = 1; i < k; i++)
		{
			double dist;
			sum = 0.0;
			for(int j = 0; j < values; j++)
			{
				sum += pow(clusters[i].getValue(j) - pt.getValue(j), 2.0);
			}
			dist = sqrt(sum);
			if(dist < minDistance)
			{
				minDistance = dist;
				clusterCenter = i;
			}
		}
		return clusterCenter;
	}
	public:
		KMeans(int k, int points, int values, int iter)
		{
			this->k = k;
			this->points = points;
			this->values = values;
			this->iterations = iter;
		}
		void run(vector<Point>&);
};
void KMeans::run(vector<Point>& pt)
{
	if(this->k > this->points)
		return;
	vector<int> indexes;
	for(int i = 0; i < this->k; i++)
	{
		while(true)
		{
			int point = rand() % points;
			if(find(indexes.begin(), indexes.end(), point) == indexes.end())
			{
				indexes.push_back(point);
				pt[point].setCluster(i);
				Cluster cluster(i, pt[point]);
				clusters.push_back(cluster);
				break;
			}
		}
	}
	int iter = 1;
	while(true)
	{
		bool isDone = true;
		for(int i = 0; i < this->points; i++)
		{
			int old = pt[i].getCluster();
			int nearest = getNearestCenter(pt[i]);
			if(old != nearest)
			{
				if(old != -1)
				{
					clusters[old].removePoint(pt[i].getID());
				}
				pt[i].setCluster(nearest);
				clusters[nearest].addPoint(pt[i]);
				isDone = false;
			}
		}
		for(int i = 0; i < k; i++)
		{
			for(int j = 0; j < values; j++)
			{
				int clusterSize = clusters[i].getTotal();
				double sum = 0.0;
				if(clusterSize > 0)
				{
					for(int p = 0; p < clusterSize; p++)
					{
						sum += clusters[i].getPoint(p).getValue(j);
					}
					clusters[i].setValue(j, sum / clusterSize);
				} 
			}
		}
		if(isDone == true || iter >= iterations)
			break;
		iter++;
		for(int i = 0; i < k; i++)
		{
			int total_pts = clusters[i].getTotal();
			cout << "Cluster " << clusters[i].getID() + 1 << "\n";
			for(int j = 0; j < total_pts; j++)
			{
				cout << "Point " << clusters[i].getPoint(j).getID() + 1 << " ";
				for(int p = 0; p < values; p++)
				{
					cout << clusters[i].getPoint(j).getValue(p) << " ";
				}
				string ptName = clusters[i].getPoint(j).getName();
				if(ptName != "")
					cout << "-" << ptName;
				cout << "\n";
				for(int j = 0; j < values; j++)
					cout << clusters[i].getValue(j) << " ";
				cout << "\n";
			}
		}	
	}
}
int main()
{
	int totalValues, totalPoints, k, iter, name;
	cout << "Enter the total Points, total Values, k, iter, name in this order\n";	
	cin >> totalPoints >> totalValues >> k >> iter >> name;
	vector<Point> pts;
	string ptname;
	for(int i = 0; i < totalPoints; i++)
	{
		vector<double> values;
		for(int j = 0; j < totalValues; j++)
		{
			double value; 
			cin >> value;
			values.push_back(value);
		}
		if(name)
		{
			cin >> ptname;
			Point p(i, values, ptname);
			pts.push_back(p);
		}
		else
		{
			Point p(i, values);
			pts.push_back(p);
		}
	}
	KMeans km(k, totalPoints, totalValues, iter);
	km.run(pts);
	return 0;
}
