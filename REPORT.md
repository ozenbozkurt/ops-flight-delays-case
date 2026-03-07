# Executive Summary

This case analyzes U.S. 2024 flight delay patterns and translates the findings into operational actions. The focus is on where delay burden concentrates, which routes show elevated risk, which delay reasons dominate, and what should be prioritized operationally.

The analysis indicates that delay burden is concentrated rather than evenly distributed. A limited number of months, origins, carriers, and routes account for a disproportionate share of operational underperformance. This supports a targeted intervention model rather than a broad network-wide response.

Overall on-time performance is approximately **80.04%**. The weakest month in the sample is **2024-07**, with the highest observed delay pressure across both EDA and operations metrics. The dominant delay driver is **late_aircraft_delay**, accounting for approximately **41.98%** of total delay-reason share. At route level, **SFO–LAX** appears as the highest-risk route in the sample, with **28.77% late rate** and **15.93 minutes average delay**.

# Objective

- Identify where delays concentrate
- Detect high-risk routes
- Understand dominant delay drivers
- Translate findings into operational recommendations

# Data and Approach

- **Source:** 2024 U.S. flight records sampled across 12 months
- **Method:** reproducible pipeline combining sampling, EDA, operations analysis, and chart generation
- **Outputs:** summary tables, route/origin/carrier rankings, delay-reason share, and visual trend charts

# Main Findings

## 1. Overall on-time performance
Overall on-time performance is approximately **80.04%**.

## 2. Seasonal pressure and worst month
The weakest month in the analyzed sample is **2024-07**.

- EDA worst-month metric: **22.67**
- Operations late-rate worst month: **29.4% late rate**

This suggests a clear seasonal concentration of operational pressure.

## 3. Dominant delay driver
The largest delay-reason category is **late_aircraft_delay**, representing approximately **41.98%** of delay share.

This is operationally important because it suggests that network delay propagation and aircraft rotation issues may be more critical than isolated local bottlenecks.

## 4. Highest-risk route
The highest-risk route identified in the sample is **SFO–LAX**.

- Late rate: **28.77%**
- Average delay: **15.93 minutes**

This route should be treated as a priority monitoring corridor rather than being hidden inside network-wide averages.

## 5. Concentration indicators
Operational underperformance is concentrated rather than evenly spread.

- Top origin: **MIA (22.2)**
- Top carrier: **AA (20.44)**

These values indicate that a relatively small number of entities may be driving a meaningful share of observed delay burden.

# Operational Risks

## Origin-driven underperformance
Repeated weak performance at specific origin stations can create downstream delay propagation across the network.

## Carrier volatility
Persistent carrier-level underperformance may indicate structural planning or execution issues rather than isolated events.

## Route fragility
Routes that repeatedly appear in the risk profile may require schedule review, turnaround review, or targeted resource allocation.

## Misallocated intervention effort
If all delay burden is treated as a single generic problem, mitigation effort may be directed at the wrong operational bottlenecks.

# Recommendations

## 1. Attack the primary delay driver: late_aircraft_delay
- Introduce tighter aircraft rotation buffers on critical turns, especially in peak months.
- Pre-position spare aircraft or crews at high-risk hubs during summer surge periods.
- Improve turnaround predictability through better gate staffing, pushback coordination, and ground-service discipline.

## 2. Build a July surge-operations playbook
- Treat **2024-07** style periods as seasonal operational stress windows.
- Add buffer capacity, increase dispatch readiness, and prioritize on-time critical legs.
- Re-rank routes by late rate during peak periods and allocate contingency resources accordingly.

## 3. Apply route-level risk management to SFO–LAX
- Flag **SFO–LAX** for active monitoring.
- Track late-rate movement in near real time.
- Use targeted schedule padding or operational interventions only where route-specific evidence supports it.

## 4. Target concentration points instead of using blanket responses
- Review repeatedly underperforming origins separately.
- Distinguish airport-driven congestion from carrier-wide execution issues.
- Use delay-reason share to prioritize the right class of intervention.

# Artifacts Produced

## Tables
- `outputs/by_month_metrics.csv`
- `outputs/worst_origins.csv`
- `outputs/worst_carriers.csv`
- `outputs/top_risky_routes.csv`
- `outputs/delay_reason_share.csv`

## Charts
- `outputs/avg_delay_by_month.png`
- `outputs/late_rate_by_month.png`
- `outputs/dep_delay_hist.png`
- `outputs/avg_delay_by_dayofweek.png`

# Conclusion

This case shows that delay burden should be managed as a concentrated operational problem, not as a uniform network condition. The findings suggest that route-level fragility, seasonal stress periods, and propagated aircraft delay are more useful decision points than generic average-delay reporting.

The practical implication is clear: operations teams should focus on repeated weak points, build targeted surge responses, and avoid wasting mitigation effort on blanket actions that do not address the actual delay structure.
