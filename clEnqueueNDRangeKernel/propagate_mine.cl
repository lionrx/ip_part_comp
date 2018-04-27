/* propagate.cl */
#define MATH_PI 3.14159265358979323846

__kernel void propagate(
	__global float4* oldPosition,
	__global float4* newPosition,
	__global float4* oldVelocity,
	__global float4* newVelocity,
	// Mass in Position
	// Temp in Velocity
	// Both stored in w
	const float tau, //4
	const float A, //5
	const float a, //6
	const float B, //7
	const float b, //8
	const float C, //9
	const float c, //10
	const float timeStep, //11
	const float C_l, //12
	const float T_g, //13
	const float P_atm, //14
	const float P_g, //15
	const float rho, //16
	const float R, //17
	const float W_c, //18
	const float W_v, //19
	const float T_B, //20
	const float rho_g, //21
	const float TWB, //22
	const double mu, //23
	const float Y_g //24
)
{



  // get the global id for this work item
	int gid = get_global_id(0);

	// pick the particle for which we will calculate the new position
	float4 pos = oldPosition[gid];
	float4 vel = oldVelocity[gid];

	// initilize local flow velocity to 0
	float4 flow_vel = (float4)(0.0, 0.0, 0.0, 0.0);

	// calculate local flow velocity
	flow_vel.x = A * cos(a * (pos.x + (3.14159 / (a * 2)))) * sin(b * (pos.y + (3.14159 / (a * 2)))) * sin(c * (pos.z + (3.14159 / (a * 2))));
	flow_vel.y = B * sin(a * (pos.x + (3.14159 / (a * 2)))) * cos(b * (pos.y + (3.14159 / (a * 2)))) * sin(c * (pos.z + (3.14159 / (a * 2))));
	flow_vel.z = C * sin(a * (pos.x + (3.14159 / (a * 2)))) * sin(b * (pos.y + (3.14159 / (a * 2)))) * cos(c * (pos.z + (3.14159 / (a * 2))));

	// extract mass and temperature of particle, and calculate diameter and dynamic time constant
	double current_m = pos.w / 1E8;			//mass must be divided by 1E8 for calculations
	double current_T = vel.w;
	double dpart = (current_m / rho)*(3.0 / 4.0);
	double current_D = 2 * pow(((current_m / rho)*(3.0/4.0) / MATH_PI), (1.0/3.0));	// current diameter
	double tau_d = rho*pow(current_D, 2.0) / (18 * mu);

	// velocity loop
	vel.x += (timeStep / tau) * (flow_vel.x - vel.x);
	vel.y += (timeStep / tau) * (flow_vel.y - vel.y) + (-0.001 * timeStep);
	vel.z += (timeStep / tau) * (flow_vel.z - vel.z);


	// displacement loop
	pos.x += (timeStep * (vel.x + oldVelocity[gid].x) / 2);
	pos.y += (timeStep * (vel.y + oldVelocity[gid].y) / 2);
	pos.z += (timeStep * (vel.z + oldVelocity[gid].z) / 2);

	// calculations for mass/temp

	double us = fabs(sqrt((pow(vel.x, 2) + pow(vel.y, 2) + pow(vel.z, 2))) - sqrt((pow(flow_vel.x, 2) + pow(flow_vel.y, 2) + pow(flow_vel.z, 2)))); // slip velocity

	double lambda_g = 3.227 * 1E-3 + 8.3894 * 1E-5 *TWB - 1.9858 * 1E-8 * pow(TWB, 2.0f);
	double Pr_g = 0.815 - 4.958 * 1E-4 * TWB + 4.514 * 1E-7 * TWB * TWB;
	double Sc_g = Pr_g;
	double cp_g = Pr_g*lambda_g / mu;

	double theta1 = cp_g / C_l;
	double theta2 = W_c / W_v;
	double L_v = 5.1478 * 1E5 * pow((1 - TWB / 512.0), 0.3861);					
	double X_seq = (P_atm / P_g)*(exp(L_v*W_v*((1.0 / (double)T_B) - (1.0 / current_T)) / R));
	double Y_seq = X_seq / (X_seq + (theta2*(1.0 - X_seq)));
	double B_meq = (Y_seq - Y_g) / (1 - Y_seq);

	double Re_d = rho_g*us*current_D / mu;
	double Nu = 2 + 0.552 * pow(Re_d, 0.5) * pow(Pr_g, (1.0 / 3.0));
	double Sh = 2 + 0.552 * pow(Re_d, 0.5) * pow(Sc_g, (1.0 / 3.0));
	tau_d = rho * current_D * current_D / (18 * mu);


	// mass and temperature loops
	double mdot_dVALUE = (-1 * Sh * current_m * B_meq) / (3 * Sc_g * tau_d);
	float mass_change = 1E8 * mdot_dVALUE * timeStep;								//multiplied by 1E8 for storage as a float
	float temp_change = timeStep * ((1.0 / 3.0) * (Nu / Pr_g) * (theta1 / tau_d) * (T_g - current_T) + (L_v / C_l) * (mdot_dVALUE / current_m));			
	pos.w += mass_change;
	vel.w += temp_change;

	// update values
	newPosition[gid] = pos;
	newVelocity[gid] = vel;
}
