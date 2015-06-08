package edu.stsci.mast.osdd.rest;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;

@Path("/deliverData")
public class DeliverData {

	@GET
	@Path("/missions/{missions}/observations/{observations}")
	public String get(@PathParam("missions") String missionsParam, @PathParam("observations") String observationsParam) {

		// command line should look like:
		// python deliver_data.py -m 'kepler' -o 'kplr012644769_lc_Q111111111111111111'
		Process proc = runPython(deliverDataCommand(parseParams(missionsParam, observationsParam)));
		
		//for (String s: deliverDataCommand(parseParams(missionsParam, observationsParam))) {
		//	System.out.println(s);
		//}

		BufferedReader stdInput = new BufferedReader(new InputStreamReader(proc.getInputStream()));

		String s = null;
		StringBuilder sb = new StringBuilder();
		try {
			while ((s = stdInput.readLine()) != null) {
				System.out.println(s);
				sb.append(s);
			}
		} catch (IOException e) {
			e.printStackTrace();
		}

		System.out.print(sb);
		return sb.toString();
	}

	private Process runPython(String[] commands) {
		ProcessBuilder pb = new ProcessBuilder(commands);
		pb.directory(new File("/Users/cfreas/MASTDataDelivery"));
		Process proc = null;
		try {
			proc = pb.start();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return proc;
	}

	private String[] deliverDataCommand(String[] params) {
		List<String> commands = new ArrayList<String>();
		commands.add("/sw/bin/python");
		commands.add("deliver_data.py");
		commands.addAll(Arrays.asList(params));
		return commands.toArray(new String[commands.size()]);
	}

	private String[] parseParams(String missionsParam, String observationsParam) {
		String[] missions = missionsParam.split(",");
		String[] observations = observationsParam.split(",");
		List<String> params = new ArrayList<String>();
		params.add("-m");
		if (missions.length == 0 || observations.length == 0) {
			throw new RuntimeException("Must have at least one mission & at least one observation.");
		} else if (missions.length > 1 && (missions.length != observations.length)) {
			throw new RuntimeException("When multiple missions specified, must have equal number of observations.");
		} else if (missions.length == 1) {
			for (int i = 0; i < observations.length; i++) {
				params.add(missions[0]);
			}
		} else if (missions.length > 1) {
			params.addAll(Arrays.asList(missions));
		}
		params.add("-o");
		params.addAll(Arrays.asList(observations));
		
		return params.toArray(new String[params.size()]);
	}
}
