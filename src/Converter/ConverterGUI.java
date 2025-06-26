	package Converter;
	
	import javax.swing.*;
	import java.awt.*;
	import java.awt.event.*;
	import java.io.*;
	
	public class ConverterGUI extends JFrame {
	
	    private JLabel titleLabel, fileLabel;
	    private JButton jsonToYamlButton, yamlToJsonButton, browseButton, resetButton;
	    private File[] selectedFiles;
	
	    public ConverterGUI() {
	        setTitle("JSON <-> YAML Converter");
	        setSize(550, 300);
	        setLayout(new FlowLayout(FlowLayout.CENTER, 20, 15));
	        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	
	        setLookAndFeel(); // 🌟 Fancy look
	
	        // Components
	        titleLabel = new JLabel("Select up to 10 files and choose an action:");
	        titleLabel.setFont(new Font("Arial", Font.BOLD, 16));
	        fileLabel = new JLabel("No files selected");
	
	        browseButton = new JButton("📁 Browse Files");
	        jsonToYamlButton = new JButton("🔄 JSON to YAML");
	        yamlToJsonButton = new JButton("🔁 YAML to JSON");
	        resetButton = new JButton("❌ Reset");
	
	        add(titleLabel);
	        add(browseButton);
	        add(fileLabel);
	        add(jsonToYamlButton);
	        add(yamlToJsonButton);
	        add(resetButton);
	
	        // 📁 File Chooser
	        browseButton.addActionListener(e -> {
	            JFileChooser fileChooser = new JFileChooser();
	            fileChooser.setMultiSelectionEnabled(true);
	            int result = fileChooser.showOpenDialog(ConverterGUI.this);
	            if (result == JFileChooser.APPROVE_OPTION) {
	                selectedFiles = fileChooser.getSelectedFiles();
	                if (selectedFiles.length > 10) {
	                    JOptionPane.showMessageDialog(this, "Please select up to 10 files only.", "Limit Exceeded", JOptionPane.WARNING_MESSAGE);
	                    selectedFiles = null;
	                    fileLabel.setText("No files selected");
	                } else {
	                    StringBuilder names = new StringBuilder("<html>Selected Files:<br>");
	                    for (File f : selectedFiles) {
	                        names.append(f.getName()).append("<br>");
	                    }
	                    names.append("</html>");
	                    fileLabel.setText(names.toString());
	                }
	            }
	        });
	
	        // 🔄 JSON → YAML
	        jsonToYamlButton.addActionListener(e -> {
	            if (selectedFiles != null && selectedFiles.length > 0) {
	                int successCount = 0;
	                for (File file : selectedFiles) {
	                    if (file.getName().endsWith(".json")) {
	                        boolean success = runPythonScript("j2y.py", file.getAbsolutePath());
	                        if (success) successCount++;
	                    }
	                }
	                JOptionPane.showMessageDialog(this, successCount + " JSON file(s) converted to YAML.", "Conversion Complete", JOptionPane.INFORMATION_MESSAGE);
	            } else {
	                JOptionPane.showMessageDialog(this, "Please select JSON files first.", "No Files Selected", JOptionPane.WARNING_MESSAGE);
	            }
	        });
	
	        // 🔁 YAML → JSON
	        yamlToJsonButton.addActionListener(e -> {
	            if (selectedFiles != null && selectedFiles.length > 0) {
	                int successCount = 0;
	                for (File file : selectedFiles) {
	                    if (file.getName().endsWith(".yaml") || file.getName().endsWith(".yml")) {
	                        boolean success = runPythonScript("y2j.py", file.getAbsolutePath());
	                        if (success) successCount++;
	                    }
	                }
	                JOptionPane.showMessageDialog(this, successCount + " YAML file(s) converted to JSON.", "Conversion Complete", JOptionPane.INFORMATION_MESSAGE);
	            } else {
	                JOptionPane.showMessageDialog(this, "Please select YAML files first.", "No Files Selected", JOptionPane.WARNING_MESSAGE);
	            }
	        });
	
	        // ❌ Reset
	        resetButton.addActionListener(e -> {
	            selectedFiles = null;
	            fileLabel.setText("No files selected");
	        });
	
	        setVisible(true);
	    }
	
	    private boolean runPythonScript(String scriptName, String filePath) {
	        try {
	            ProcessBuilder pb = new ProcessBuilder("python", scriptName, filePath);
	            pb.directory(new File(System.getProperty("user.dir")));
	            pb.redirectErrorStream(true);
	            Process process = pb.start();
	
	            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
	            String line;
	            while ((line = reader.readLine()) != null) {
	                System.out.println(line); // Eclipse console
	            }
	
	            int exitCode = process.waitFor();
	            return exitCode == 0;
	
	        } catch (Exception ex) {
	            ex.printStackTrace();
	            return false;
	        }
	    }
	
	    private void setLookAndFeel() {
	        try {
	            for (UIManager.LookAndFeelInfo info : UIManager.getInstalledLookAndFeels()) {
	                if ("Nimbus".equals(info.getName())) {
	                    UIManager.setLookAndFeel(info.getClassName());
	                    break;
	                }
	            }
	        } catch (Exception e) {
	            System.out.println("⚠️ Nimbus LookAndFeel not available.");
	        }
	    }
	
	    public static void main(String[] args) {
	        SwingUtilities.invokeLater(ConverterGUI::new);
	    }
	}
