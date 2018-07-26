/* CLI markdown.config.js file example */

const execSync = require('child_process').execSync
var fs = require('fs');

module.exports = {
  transforms: {
    COMMAND_OUTPUT(content, options) {
      make_help_output = execSync(options.command, {});
      return `
\`\`\`.{shell}
$ ${options.displayName}

${make_help_output}
\`\`\`
      `;
    },
    IMPORT_MD(content, options) {
      var contents = fs.readFileSync(options.src, 'utf8');
      return contents;
    }
  },
};
